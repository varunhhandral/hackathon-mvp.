import io
import re
from docx import Document
from docx.shared import Pt, RGBColor
import numpy as np
from openpyxl.styles import Font, PatternFill
import pandas as pd
import pdfplumber
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Senior Data Entry & Document Conversion Studio",
    page_icon="🗂️",
    layout="wide",
)


@st.cache_resource
def load_ocr_engine():
  return RapidOCR()


# --- COLOUR PALETTE MAPPING ---
PALETTES = {
    "Corporate Slate Navy": {"hex": "1B365D", "rgb": (27, 54, 93)},
    "Executive Charcoal": {"hex": "2C3E50", "rgb": (44, 62, 80)},
    "Emerald Finance": {"hex": "1E6B52", "rgb": (30, 107, 82)},
    "Royal Burgundy": {"hex": "6B1E3B", "rgb": (107, 30, 59)},
}

# --- SIDEBAR CONTROLS ---
with st.sidebar:
  st.header("⚙️ Senior Data Entry Controls")

  output_format = st.selectbox(
      "1. Output Deliverable Format",
      ["Microsoft Word (.docx)", "Microsoft Excel (.xlsx)"],
  )

  deep_clean = st.checkbox(
      "2. Enable Deep Data Cleaning (Deduplicate, Trim, Fix Numbers & Dates)",
      value=True,
  )

  sequence_rule = st.selectbox(
      "3. Sequence & Layout Ordering",
      [
          "Preserve Exact Document / Page Sequence",
          "Sort Alphabetically by First Column",
          "Group by Category / Section",
      ],
  )

  apply_palette = st.checkbox("4. Apply Custom Colour Palette", value=True)
  palette_name = st.selectbox("Select Colour Palette", list(PALETTES.keys()))

  st.subheader("5. Typography & Layout Rules")
  font_family = st.selectbox(
      "Font Family", ["Arial", "Calibri", "Times New Roman", "Verdana"]
  )
  font_size = st.number_input(
      "Font Size (pt)", min_value=8, max_value=24, value=11
  )
  preserve_headers_footers = st.checkbox(
      "Preserve Headers, Footers & Page Numbers", value=True
  )


# --- DETERMINISTIC DATA CLEANING ENGINE ---
def clean_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
  flags = []
  df = df.copy()

  # 1. Clean column headers
  df.columns = [re.sub(r"\s+", " ", str(c)).strip() for c in df.columns]

  # 2. Drop completely empty rows and columns
  df.dropna(how="all", inplace=True)
  df.dropna(axis=1, how="all", inplace=True)

  # 3. Trim whitespace inside string cells
  for col in df.select_dtypes(include=["object", "string"]).columns:
    df[col] = df[col].apply(
        lambda x: re.sub(r"\s+", " ", x).strip() if isinstance(x, str) else x
    )

    # Attempt date standardization if column name hints at a date
    if any(k in col.lower() for k in ["date", "dob", "time", "created"]):
      parsed = pd.to_datetime(df[col], errors="coerce")
      if parsed.notna().mean() > 0.6:
        df[col] = parsed.dt.strftime("%Y-%m-%d").fillna(df[col])

    # Attempt numeric cleanup if values look like currency/formatted numbers
    sample = df[col].dropna().astype(str)
    if (
        len(sample) > 0
        and sample.str.match(r"^[₹$€£]?\s*-?[\d,]+(\.\d+)?$").mean() > 0.7
    ):
      cleaned_num = (
          df[col].astype(str).str.replace(r"[₹$€£,\s]", "", regex=True)
      )
      try:
        df[col] = pd.to_numeric(cleaned_num)
      except (ValueError, TypeError):
        pass
  # 4. Deduplicate rows
  before_count = len(df)
  df.drop_duplicates(inplace=True)
  removed = before_count - len(df)
  if removed > 0:
    flags.append(f"Removed {removed} duplicate row(s).")

  # 5. Flag rows with missing values for quick QA
  missing_rows = df[df.isna().any(axis=1)].index.tolist()
  if missing_rows:
    preview_idx = ", ".join(str(i + 1) for i in missing_rows[:10])
    extra = (
        f" (+{len(missing_rows) - 10} more)" if len(missing_rows) > 10 else ""
    )
    flags.append(f"Rows with blank/missing cells: {preview_idx}{extra}")

  return df.reset_index(drop=True), flags


def apply_ordering(df: pd.DataFrame) -> pd.DataFrame:
  if df.empty or len(df.columns) == 0:
    return df
  first_col = df.columns[0]
  if sequence_rule == "Sort Alphabetically by First Column":
    return df.sort_values(
        by=first_col, key=lambda s: s.astype(str).str.lower()
    ).reset_index(drop=True)
  elif sequence_rule == "Group by Category / Section":
    # Pick lowest-cardinality text column to group by, fallback to first column
    cat_cols = [
        c
        for c in df.columns
        if 1 < df[c].nunique(dropna=True) <= max(20, len(df) // 5)
    ]
    group_col = cat_cols[0] if cat_cols else first_col
    return df.sort_values(
        by=group_col, key=lambda s: s.astype(str).str.lower()
    ).reset_index(drop=True)
  return df


# --- LOCAL FILE EXTRACTION (NO API KEY) ---
def extract_local_file(uploaded_file) -> tuple[pd.DataFrame, str]:
  file_bytes = uploaded_file.getvalue()
  file_name = uploaded_file.name.lower()
  metadata_notes = []

  if file_name.endswith(".csv"):
    df = pd.read_csv(io.BytesIO(file_bytes))
    metadata_notes.append(f"Source: CSV ({len(df)} raw rows)")

  elif file_name.endswith(".xlsx"):
    excel_file = pd.ExcelFile(io.BytesIO(file_bytes))
    df = excel_file.parse(excel_file.sheet_names[0])
    metadata_notes.append(
        f"Source: Excel Sheet '{excel_file.sheet_names[0]}' ({len(df)} raw"
        " rows)"
    )

  elif file_name.endswith(".pdf"):
    all_tables = []
    text_lines = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
      metadata_notes.append(f"Total Pages: {len(pdf.pages)}")
      for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        if tables:
          for t in tables:
            if len(t) > 1:
              headers = [
                  str(h).strip() if h else f"Col_{i+1}"
                  for i, h in enumerate(t[0])
              ]
              page_df = pd.DataFrame(t[1:], columns=headers)
              if preserve_headers_footers:
                page_df["Page_No"] = page_num
              all_tables.append(page_df)
        else:
          raw_text = page.extract_text() or ""
          for line in raw_text.splitlines():
            if line.strip():
              text_lines.append({"Page_No": page_num, "Extracted_Text": line})

    if all_tables:
      df = pd.concat(all_tables, ignore_index=True)
    else:
      df = pd.DataFrame(text_lines)

  else:
    # Scanned Image OCR (PNG, JPG, WEBP)
    ocr = load_ocr_engine()
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    result, _ = ocr(np.array(img))
    if result:
      rows = []
      for item in result:
        text = item[1]
        confidence = round(float(item[2]) * 100, 1)
        rows.append(
            {"Extracted_Text": text, "OCR_Confidence_%": f"{confidence}%"}
        )
      df = pd.DataFrame(rows)
      metadata_notes.append(
          f"OCR Extracted {len(df)} text blocks from scanned image."
      )
    else:
      df = pd.DataFrame(columns=["Extracted_Text"])
      metadata_notes.append("No readable text detected in image.")

  return df, " | ".join(metadata_notes)


# --- DELIVERABLE BUILDERS ---
def build_excel(
    df: pd.DataFrame, title: str, summary: str, hex_color: str
) -> bytes:
  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Cleaned_Data", startrow=2)
    ws = writer.sheets["Cleaned_Data"]

    ws["A1"] = title
    ws["A1"].font = Font(
        name=font_family, size=font_size + 3, bold=True, color=hex_color
    )
    if preserve_headers_footers and summary:
      ws["A2"] = summary
      ws["A2"].font = Font(name=font_family, size=font_size - 1, italic=True)

    header_fill = PatternFill(
        start_color=hex_color, end_color=hex_color, fill_type="solid"
    )
    header_font = Font(
        name=font_family, size=font_size, bold=True, color="FFFFFF"
    )
    for col_idx in range(1, len(df.columns) + 1):
      cell = ws.cell(row=3, column=col_idx)
      if apply_palette:
        cell.fill = header_fill
        cell.font = header_font
      else:
        cell.font = Font(name=font_family, size=font_size, bold=True)

  return buffer.getvalue()


def build_word(
    df: pd.DataFrame, title: str, summary: str, rgb_color: tuple[int, int, int]
) -> bytes:
  doc = Document()

  style = doc.styles["Normal"]
  style.font.name = font_family
  style.font.size = Pt(font_size)

  heading = doc.add_heading(title, level=1)
  run = heading.runs[0]
  run.font.name = font_family
  run.font.size = Pt(font_size + 4)
  if apply_palette:
    run.font.color.rgb = RGBColor(*rgb_color)

  if preserve_headers_footers and summary:
    p = doc.add_paragraph(summary)
    p.runs[0].italic = True

  table = doc.add_table(rows=1, cols=len(df.columns))
  table.style = "Table Grid"

  hdr_cells = table.rows[0].cells
  for i, col_name in enumerate(df.columns):
    hdr_cells[i].text = str(col_name)
    for run in hdr_cells[i].paragraphs[0].runs:
      run.bold = True
      run.font.name = font_family
      run.font.size = Pt(font_size)
      if apply_palette:
        run.font.color.rgb = RGBColor(*rgb_color)

  # Cap Word table rows to 500 to avoid sluggish browser/Word rendering on huge CSVs
  export_df = df.head(500)
  for _, row in export_df.iterrows():
    row_cells = table.add_row().cells
    for i, val in enumerate(row):
      row_cells[i].text = "" if pd.isna(val) else str(val)
      for run in row_cells[i].paragraphs[0].runs:
        run.font.name = font_family
        run.font.size = Pt(font_size)

  if len(df) > 500:
    doc.add_paragraph(
        f"Note: Showing first 500 of {len(df)} rows. Export as .xlsx for the"
        " full dataset."
    )

  buffer = io.BytesIO()
  doc.save(buffer)
  return buffer.getvalue()


# --- MAIN UI ---
st.title("🗂️ Universal Data Entry & Client Deliverable Studio")
st.markdown(
    "Upload **any client file** (`PDF`, `PNG/JPG Scanned Image`, `CSV`, or"
    " `XLSX`), configure cleaning, sequence, font, and optional colour palette"
    " rules, and export ready-to-deliver **Excel** or **Word (`.docx`)** files"
    " — **100% locally with zero API keys**."
)

col1, col2 = st.columns(2)
with col1:
  uploaded_files = st.file_uploader(
      "Upload Client Source Files (PDF, Scanned Images, CSV, XLSX)",
      type=["pdf", "png", "jpg", "jpeg", "webp", "csv", "xlsx"],
      accept_multiple_files=True,
  )
with col2:
  client_instructions = st.text_area(
      "Client Brief / Deliverable Notes (Included in Report Header)",
      placeholder=(
          "Add project title or client notes (e.g., 'Q3 Zomato Cleaned"
          " Dataset - Prepared for Client Review')..."
      ),
      height=135,
  )

if st.button("🚀 Process All Client Files & Generate Deliverables"):
  if not uploaded_files:
    st.warning("Please upload at least one client file.")
  else:
    st.session_state["results"] = []

    for f in uploaded_files:
      with st.spinner(f"Processing `{f.name}`..."):
        try:
          df, meta_summary = extract_local_file(f)
          flags = []

          if deep_clean:
            df, flags = clean_dataframe(df)

          df = apply_ordering(df)

          title = (
              client_instructions.strip().splitlines()[0][:80]
              if client_instructions.strip()
              else f.name.rsplit(".", 1)[0].replace("_", " ").title()
          )

          st.session_state["results"].append({
              "filename": f.name,
              "title": title,
              "summary": meta_summary,
              "df": df,
              "flags": flags,
          })
        except Exception as e:
          st.error(f"Failed to process `{f.name}`: {e}")

# --- HUMAN-IN-THE-LOOP REVIEW & DOWNLOAD ---
if "results" in st.session_state and st.session_state["results"]:
  st.divider()
  st.subheader("✅ Review, Edit & Export Client Deliverables")

  palette = PALETTES[palette_name]

  for idx, item in enumerate(st.session_state["results"]):
    with st.expander(
        f"📄 {item['filename']} — {len(item['df'])} rows", expanded=True
    ):
      if item["flags"]:
        st.info(
            "**Data Cleaning & Quality Report:**\n- "
            + "\n- ".join(item["flags"])
        )

      edited_df = st.data_editor(
          item["df"],
          key=f"editor_{idx}",
          width="stretch",
          num_rows="dynamic",
      )

      base_name = item["filename"].rsplit(".", 1)[0]

      if output_format == "Microsoft Word (.docx)":
        doc_bytes = build_word(
            edited_df, item["title"], item["summary"], palette["rgb"]
        )
        st.download_button(
            label=f"⬇️ Download {base_name}_cleaned.docx",
            data=doc_bytes,
            file_name=f"{base_name}_cleaned.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"dl_doc_{idx}",
        )
      else:
        xlsx_bytes = build_excel(
            edited_df, item["title"], item["summary"], palette["hex"]
        )
        st.download_button(
            label=f"⬇️ Download {base_name}_cleaned.xlsx",
            data=xlsx_bytes,
            file_name=f"{base_name}_cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"dl_xlsx_{idx}",
        )
