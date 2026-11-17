import io
import json
import os
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from google import genai
from google.genai import types
from openpyxl.styles import Alignment, Font, PatternFill
import pandas as pd
from PIL import Image
from pypdf import PdfReader
import streamlit as st

st.set_page_config(
    page_title="Senior Data Entry & Document Conversion Studio",
    layout="wide",
)

PALETTES = {
    "None (Plain Clean Office Format)": None,
    "Corporate Slate Navy": {
        "header_bg": "1E293B",
        "sub_bg": "D9E2EC",
        "zebra_bg": "F8FAFC",
        "header_fg": "FFFFFF",
    },
    "Executive Emerald Green": {
        "header_bg": "065F46",
        "sub_bg": "D1FAE5",
        "zebra_bg": "F0FDF4",
        "header_fg": "FFFFFF",
    },
    "Royal Burgundy & Warm Grey": {
        "header_bg": "7F1D1D",
        "sub_bg": "FEE2E2",
        "zebra_bg": "FAF5F5",
        "header_fg": "FFFFFF",
    },
    "Classic Deep Indigo": {
        "header_bg": "312E81",
        "sub_bg": "E0E7FF",
        "zebra_bg": "F5F7FF",
        "header_fg": "FFFFFF",
    },
}

st.title("🗂️ Universal Data Entry & Client Deliverable Studio")
st.markdown(
    "Upload **any client file** (`PDF`, `PNG/JPG Scanned Image`, `CSV`, or"
    " `XLSX`), paste the exact **client brief**, configure cleaning, sequence,"
    " font, and optional colour palette rules, and export ready-to-deliver"
    " **Excel** or **Word (`.docx`)** files."
)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
  st.header("⚙️ Senior Data Entry Controls")

  # Auto-detect key from Streamlit secrets or environment variables if available
  default_key = ""
  try:
    if "GEMINI_API_KEY" in st.secrets:
      default_key = st.secrets["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in os.environ:
      default_key = os.environ["GEMINI_API_KEY"]
  except Exception:
    pass

  api_key = st.text_input(
      "Gemini API Key", value=default_key, type="password"
  )

  output_format = st.selectbox(
      "1. Output Deliverable Format",
      [
          "Microsoft Word (.docx)",
          "Microsoft Excel (.xlsx)",
          "Both (.docx & .xlsx)",
      ],
  )

  enable_cleaning = st.checkbox(
      "2. Enable Deep Data Cleaning (Deduplicate, Trim, Fix Numbers & Dates)",
      value=True,
  )

  sequence_mode = st.selectbox(
      "3. Sequence & Layout Ordering",
      [
          "Preserve Exact Document / Page Sequence",
          "ID Sequence (Natural Numeric Order)",
          "Chronological Date Sequence (Oldest → Newest)",
          "Category / Area / Department Grouping",
      ],
  )

  use_palette = st.checkbox("4. Apply Custom Colour Palette", value=True)
  selected_palette_name = st.selectbox(
      "Select Colour Palette",
      list(PALETTES.keys())[1:],
      disabled=not use_palette,
  )
  active_palette = PALETTES[selected_palette_name] if use_palette else None

  st.subheader("5. Typography & Layout Rules")
  font_family = st.selectbox(
      "Font Family", ["Arial", "Calibri", "Times New Roman", "Segoe UI"]
  )
  font_size = st.number_input(
      "Font Size (pt)", min_value=8, max_value=24, value=11
  )
  include_footers = st.checkbox(
      "Preserve Headers, Footers & Page Numbers", value=True
  )

# --- MAIN WORKSPACE ---
col_left, col_right = st.columns([1.2, 1])

with col_left:
  uploaded_files = st.file_uploader(
      "Upload Client Source Files (PDF, Scanned Images, CSV, XLSX)",
      type=["pdf", "png", "jpg", "jpeg", "webp", "csv", "xlsx"],
      accept_multiple_files=True,
  )

with col_right:
  client_instructions = st.text_area(
      "Client Request / Custom Formatting Instructions",
      height=155,
      placeholder=(
          "Paste client instructions here (e.g., 'Convert scanned PDFs into Word"
          " using Arial size 11, preserve footer info')..."
      ),
  )


# --- HELPER FUNCTIONS ---
def set_docx_cell_bg(cell, hex_color):
  if not hex_color:
    return
  tcPr = cell._tc.get_or_add_tcPr()
  shd = OxmlElement("w:shd")
  shd.set(qn("w:val"), "clear")
  shd.set(qn("w:color"), "auto")
  shd.set(qn("w:fill"), hex_color)
  tcPr.append(shd)


def build_docx_from_structured_json(
    doc_json, font_name, font_pt, palette, keep_footer
):
  doc = Document()
  normal_style = doc.styles["Normal"]
  normal_style.font.name = font_name
  normal_style.font.size = Pt(font_pt)

  footer_text = doc_json.get("footer", "")
  if keep_footer and footer_text:
    section = doc.sections[0]
    fp = section.footer.paragraphs[0]
    fr = fp.add_run(footer_text)
    fr.font.name = font_name
    fr.font.size = Pt(font_pt)

  for block in doc_json.get("blocks", []):
    b_type = block.get("type", "paragraph")
    if b_type == "banner":
      tbl = doc.add_table(rows=1, cols=1)
      cell = tbl.rows[0].cells[0]
      cell.width = Inches(6.5)
      bg = (
          palette["header_bg"]
          if palette
          else block.get("bg_hex", "D9E2EC").replace("#", "")
      )
      set_docx_cell_bg(cell, bg)
      p = cell.paragraphs[0]
      r = p.add_run(block.get("text", ""))
      r.font.name = font_name
      r.font.size = Pt(font_pt)
      r.bold = True
      if palette:
        r.font.color.rgb = RGBColor(255, 255, 255)
      doc.add_paragraph()

    elif b_type == "heading":
      p = doc.add_paragraph()
      r = p.add_run(block.get("text", ""))
      r.font.name = font_name
      r.font.size = Pt(font_pt)
      r.bold = True

    elif b_type == "table":
      rows_data = block.get("rows", [])
      if rows_data:
        max_cols = max(len(r) for r in rows_data)
        tbl = doc.add_table(rows=len(rows_data), cols=max_cols)
        for r_idx, row_vals in enumerate(rows_data):
          for c_idx in range(max_cols):
            val = row_vals[c_idx] if c_idx < len(row_vals) else ""
            cell = tbl.rows[r_idx].cells[c_idx]
            if r_idx == 0 and palette:
              set_docx_cell_bg(cell, palette["header_bg"])
            elif r_idx % 2 == 1 and palette:
              set_docx_cell_bg(cell, palette["zebra_bg"])
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = font_name
            run.font.size = Pt(font_pt)
            if r_idx == 0:
              run.bold = True
              if palette:
                run.font.color.rgb = RGBColor(255, 255, 255)
        doc.add_paragraph()

    else:
      p = doc.add_paragraph()
      r = p.add_run(block.get("text", ""))
      r.font.name = font_name
      r.font.size = Pt(font_pt)
      if block.get("bold", False):
        r.bold = True

  buf = io.BytesIO()
  doc.save(buf)
  return buf.getvalue()


def clean_tabular_dataframe(df, do_clean, seq_mode):
  out = df.copy()
  if do_clean:
    for col in out.select_dtypes(include=["object"]).columns:
      if "id" in col.lower():
        out[col] = out[col].astype(str).str.strip().str.upper()
      else:
        out[col] = (
            out[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )
      out[col] = out[col].replace(["Nan", "None", "Nat", ""], pd.NA)

    out = out.drop_duplicates().reset_index(drop=True)

    date_col = next((c for c in out.columns if "date" in c.lower()), None)
    if date_col:
      out["_sort_dt"] = pd.to_datetime(out[date_col], errors="coerce")
      out[date_col] = out["_sort_dt"].dt.strftime("%d %B %Y").fillna(
          "Not Specified"
      )

    word_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6}
    for col in ["Quantity", "Rating"]:
      if col in out.columns:
        out[col] = pd.to_numeric(
            out[col].replace(word_map), errors="coerce"
        ).fillna(1 if col == "Quantity" else 4.0)
        if col == "Quantity":
          out[col] = out[col].astype(int)

    for col in [
        "Item Price",
        "Delivery Fee",
        "Basic Salary",
        "Salary",
        "Price",
    ]:
      if col in out.columns:
        out[col] = (
            out[col]
            .astype(str)
            .str.replace(r"(?i)rs\.?|₹|,", "", regex=True)
            .str.strip()
        )
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)

    if all(
        c in out.columns for c in ["Quantity", "Item Price", "Delivery Fee"]
    ):
      out["Total_Revenue"] = (out["Quantity"] * out["Item Price"]) + out[
          "Delivery Fee"
      ]

    for col in out.select_dtypes(include=["object"]).columns:
      out[col] = out[col].fillna("Not Specified")

  id_col = next(
      (
          c
          for c in out.columns
          if c.lower() in ["order id", "employee id", "id"]
      ),
      None,
  )
  if "ID Sequence" in seq_mode and id_col:
    out["_id_num"] = (
        out[id_col].astype(str).str.extract(r"(\d+)").astype(float).fillna(9e9)
    )
    out = out.sort_values(by=["_id_num", id_col])
  elif "Chronological" in seq_mode and "_sort_dt" in out.columns:
    out = out.sort_values(by=["_sort_dt"])
  elif "Category" in seq_mode:
    grp = next(
        (c for c in ["Area", "Department", "Category"] if c in out.columns), None
    )
    if grp:
      out = out.sort_values(by=[grp])

  out = out.drop(
      columns=[c for c in ["_sort_dt", "_id_num"] if c in out.columns]
  ).reset_index(drop=True)
  return out


def build_styled_excel(df_main, palette, font_name, font_pt):
  output = io.BytesIO()
  with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df_main.to_excel(writer, sheet_name="Cleaned_Deliverable", index=False)
    ws = writer.sheets["Cleaned_Deliverable"]
    ws.freeze_panes = "A2"

    hdr_fill = (
        PatternFill(
            start_color=palette["header_bg"],
            end_color=palette["header_bg"],
            fill_type="solid",
        )
        if palette
        else None
    )
    zebra_fill = (
        PatternFill(
            start_color=palette["zebra_bg"],
            end_color=palette["zebra_bg"],
            fill_type="solid",
        )
        if palette
        else None
    )
    hdr_font = Font(
        name=font_name,
        size=font_pt,
        bold=True,
        color=palette["header_fg"] if palette else "000000",
    )
    body_font = Font(name=font_name, size=font_pt)

    for col_idx, col_name in enumerate(df_main.columns, 1):
      is_num = pd.api.types.is_numeric_dtype(df_main[col_name])
      align = Alignment(
          horizontal="right" if is_num else "left", vertical="center"
      )
      for row_idx in range(1, len(df_main) + 2):
        cell = ws.cell(row=row_idx, column=col_idx)
        if row_idx == 1:
          if hdr_fill:
            cell.fill = hdr_fill
          cell.font = hdr_font
          cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
          cell.font = body_font
          cell.alignment = align
          if zebra_fill and row_idx % 2 == 0:
            cell.fill = zebra_fill

    for col_cells in ws.columns:
      max_len = max(len(str(c.value or "")) for c in col_cells)
      ws.column_dimensions[col_cells[0].column_letter].width = min(
          max_len + 4, 40
      )

  return output.getvalue()


# --- EXECUTION ENGINE ---
if st.button("🚀 Process All Client Files & Generate Deliverables"):
  if not uploaded_files:
    st.warning("Please upload at least one file.")
    st.stop()

  for file in uploaded_files:
    st.markdown(f"### 📄 Processing: `{file.name}`")
    ext = file.name.split(".")[-1].lower()
    base_name = file.name.rsplit(".", 1)[0]

    if ext in ["csv", "xlsx"]:
      raw_df = (
          pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
      )
      clean_df = clean_tabular_dataframe(
          raw_df, enable_cleaning, sequence_mode
      )
      st.dataframe(clean_df, use_container_width=True, height=300)

      if "Excel" in output_format or "Both" in output_format:
        xlsx_bytes = build_styled_excel(
            clean_df, active_palette, font_family, font_size
        )
        st.download_button(
            label=f"📥 Download Cleaned Excel ({base_name}_Cleaned.xlsx)",
            data=xlsx_bytes,
            file_name=f"{base_name}_Cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"xlsx_{file.name}",
        )

      if "Word" in output_format or "Both" in output_format:
        doc_struct = {
            "footer": f"{base_name} | Client Deliverable",
            "blocks": [
                {"type": "banner", "text": f"CLEANED REPORT: {base_name}"},
                {
                    "type": "table",
                    "rows": [clean_df.columns.tolist()]
                    + clean_df.head(500).astype(str).values.tolist(),
                },
            ],
        }
        docx_bytes = build_docx_from_structured_json(
            doc_struct,
            font_family,
            font_size,
            active_palette,
            include_footers,
        )
        st.download_button(
            label=f"📥 Download Word Deliverable ({base_name}_Cleaned.docx)",
            data=docx_bytes,
            file_name=f"{base_name}_Cleaned.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            key=f"docx_{file.name}",
        )

    elif ext in ["pdf", "png", "jpg", "jpeg", "webp"]:
      if not api_key:
        st.error(
            "⚠️ Please enter your Gemini API Key in the sidebar input box"
            " above to transcribe PDFs and images."
        )
        continue

      with st.spinner(
          f"Transcribing {file.name} with senior data-entry precision..."
      ):
        try:
          client = genai.Client(api_key=api_key)
          file_bytes = file.read()
          mime_map = {
              "pdf": "application/pdf",
              "png": "image/png",
              "jpg": "image/jpeg",
              "jpeg": "image/jpeg",
              "webp": "image/webp",
          }
          prompt = f"""
            You are a senior data entry specialist with 12 years of experience.
            Transcribe EVERY word, number, table, heading, and footer from this document with 100% accuracy.
            Client instructions: {client_instructions or 'Preserve exact text, structure, tables, and footers.'}
            Cleaning enabled: {enable_cleaning}. Sequence mode: {sequence_mode}.

            Return ONLY valid JSON in this exact schema:
            {{
              "footer": "exact footer text if present, else empty string",
              "blocks": [
                {{"type": "banner", "text": "Title or top header text", "bg_hex": "D9E2EC"}},
                {{"type": "heading", "text": "Section heading"}},
                {{"type": "paragraph", "text": "Full paragraph or bullet text", "bold": false}},
                {{"type": "table", "rows": [["Col1", "Col2"], ["Val1", "Val2"]]}}
              ]
            }}
            """
          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=[
                  types.Part.from_bytes(
                      data=file_bytes, mime_type=mime_map[ext]
                  ),
                  prompt,
              ],
              config=types.GenerateContentConfig(
                  response_mime_type="application/json"
              ),
          )
          parsed = json.loads(response.text)

          st.success(
              f"Extracted {len(parsed.get('blocks', []))} structured blocks."
          )

          if "Word" in output_format or "Both" in output_format:
            docx_bytes = build_docx_from_structured_json(
                parsed,
                font_family,
                font_size,
                active_palette,
                include_footers,
            )
            st.download_button(
                label=(
                    f"📥 Download Word Deliverable"
                    f" ({base_name}_Deliverable.docx)"
                ),
                data=docx_bytes,
                file_name=f"{base_name}_Deliverable.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key=f"docx_{file.name}",
            )

          if "Excel" in output_format or "Both" in output_format:
            tables = [
                b["rows"]
                for b in parsed.get("blocks", [])
                if b.get("type") == "table" and len(b.get("rows", [])) > 1
            ]
            if tables:
              t_rows = tables[0]
              df_extracted = pd.DataFrame(t_rows[1:], columns=t_rows[0])
            else:
              df_extracted = pd.DataFrame(
                  [
                      {"Content": b.get("text", "")}
                      for b in parsed.get("blocks", [])
                      if b.get("text")
                  ]
              )
            df_extracted = clean_tabular_dataframe(
                df_extracted, enable_cleaning, sequence_mode
            )
            xlsx_bytes = build_styled_excel(
                df_extracted, active_palette, font_family, font_size
            )
            st.download_button(
                label=(
                    f"📥 Download Excel Deliverable"
                    f" ({base_name}_Deliverable.xlsx)"
                ),
                data=xlsx_bytes,
                file_name=f"{base_name}_Deliverable.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"xlsx_{file.name}",
            )

        except Exception as e:
          st.error(
              f"Error during API processing: {e}. Please check your API key"
              " and try again."
          )
