import io
from docx import Document
from docx.shared import Pt, RGBColor
from google import genai
from google.genai import types
import openpyxl
from openpyxl.styles import Font, PatternFill
import pandas as pd
from PIL import Image
from pydantic import BaseModel, Field
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Senior Data Entry & Document Conversion Studio",
    page_icon="🗂️",
    layout="wide",
)


# --- PYDANTIC SCHEMA FOR STRUCTURED OUTPUTS ---
class DataRow(BaseModel):
  cells: list[str] = Field(
      description="Values for each column in exact header order."
  )
  confidence_note: str | None = Field(
      default=None,
      description=(
          "Flag if any text in this row was blurry, illegible, or ambiguous."
      ),
  )


class ExtractedDeliverable(BaseModel):
  document_title: str = Field(
      description="Clean title for the report or spreadsheet."
  )
  summary_notes: str = Field(
      description=(
          "Brief overview or preserved header/footer metadata from the"
          " document."
      )
  )
  column_headers: list[str] = Field(
      description="Standardized column names in exact sequence."
  )
  rows: list[DataRow] = Field(
      description="All extracted data rows, cleaned and standardized."
  )


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
  api_key = st.text_input("Gemini API Key", type="password")

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


# --- EXTRACTION ENGINE ---
def process_uploaded_file(
    uploaded_file, client: genai.Client, instructions: str
) -> ExtractedDeliverable:
  file_bytes = uploaded_file.getvalue()
  mime_type = uploaded_file.type
  file_name = uploaded_file.name.lower()

  cleaning_rules = (
      "Apply deep data cleaning: trim extra whitespace, standardize all dates"
      " to YYYY-MM-DD, and clean number formatting."
      if deep_clean
      else "Extract raw values verbatim without altering date or number formats."
  )
  header_footer_rules = (
      "Include any document header, footer, or page number info inside"
      " summary_notes."
      if preserve_headers_footers
      else "Ignore page headers and footers."
  )

  prompt = f"""
    You are a Senior Data Entry Specialist. Extract all tabular and structured data from the provided file.
    
    Client Instructions: {instructions if instructions.strip() else "Extract cleanly and accurately."}
    Cleaning Rules: {cleaning_rules}
    Ordering Rule: {sequence_rule}
    Metadata Rule: {header_footer_rules}
    
    Ensure every row in `rows` has the exact same number of elements in `cells` as `column_headers`.
    If a cell is empty, use an empty string "".
    """

  # Handle CSV / XLSX directly via Pandas + Gemini structuring
  if file_name.endswith(".csv"):
    df_raw = pd.read_csv(io.BytesIO(file_bytes))
    content_payload = [prompt, f"Raw CSV Data:\n{df_raw.to_csv(index=False)}"]
  elif file_name.endswith(".xlsx"):
    df_raw = pd.read_excel(io.BytesIO(file_bytes))
    content_payload = [prompt, f"Raw Excel Data:\n{df_raw.to_csv(index=False)}"]
  elif file_name.endswith(".pdf"):
    pdf_part = types.Part.from_bytes(
        data=file_bytes, mime_type="application/pdf"
    )
    content_payload = [pdf_part, prompt]
  else:
    # Images (PNG, JPG, WEBP)
    img = Image.open(io.BytesIO(file_bytes))
    content_payload = [img, prompt]

  response = client.models.generate_content(
      model="gemini-2.5-flash",
      contents=content_payload,
      config=types.GenerateContentConfig(
          response_mime_type="application/json",
          response_schema=ExtractedDeliverable,
          temperature=0.1,
      ),
  )
  return response.parsed


# --- DELIVERABLE BUILDERS ---
def build_excel(
    df: pd.DataFrame, title: str, summary: str, hex_color: str
) -> bytes:
  buffer = io.BytesIO()
  with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Cleaned_Data", startrow=2)
    ws = writer.sheets["Cleaned_Data"]

    # Title styling
    ws["A1"] = title
    ws["A1"].font = Font(
        name=font_family, size=font_size + 3, bold=True, color=hex_color
    )
    if preserve_headers_footers and summary:
      ws["A2"] = summary
      ws["A2"].font = Font(name=font_family, size=font_size - 1, italic=True)

    # Header styling
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

  # Base document font
  style = doc.styles["Normal"]
  style.font.name = font_family
  style.font.size = Pt(font_size)

  # Title
  heading = doc.add_heading(title, level=1)
  run = heading.runs[0]
  run.font.name = font_family
  run.font.size = Pt(font_size + 4)
  if apply_palette:
    run.font.color.rgb = RGBColor(*rgb_color)

  if preserve_headers_footers and summary:
    p = doc.add_paragraph(summary)
    p.runs[0].italic = True

  # Table
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

  for _, row in df.iterrows():
    row_cells = table.add_row().cells
    for i, val in enumerate(row):
      row_cells[i].text = "" if pd.isna(val) else str(val)
      for run in row_cells[i].paragraphs[0].runs:
        run.font.name = font_family
        run.font.size = Pt(font_size)

  buffer = io.BytesIO()
  doc.save(buffer)
  return buffer.getvalue()


# --- MAIN UI ---
st.title("🗂️ Universal Data Entry & Client Deliverable Studio")
st.markdown(
    "Upload **any client file** (`PDF`, `PNG/JPG Scanned Image`, `CSV`, or"
    " `XLSX`), paste the exact **client brief**, configure cleaning, sequence,"
    " font, and optional colour palette rules, and export ready-to-deliver"
    " **Excel** or **Word (`.docx`)** files."
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
      "Client Request / Custom Formatting Instructions",
      placeholder=(
          "Paste client instructions here (e.g., 'Convert scanned PDFs into"
          " Word using Arial size 11, preserve footer info')..."
      ),
      height=135,
  )

if st.button("🚀 Process All Client Files & Generate Deliverables"):
  if not api_key:
    st.error("Please enter your Gemini API Key in the left sidebar.")
  elif not uploaded_files:
    st.warning("Please upload at least one client file.")
  else:
    client = genai.Client(api_key=api_key)
    st.session_state["results"] = []

    for f in uploaded_files:
      with st.spinner(f"Extracting & cleaning `{f.name}`..."):
        try:
          extracted = process_uploaded_file(f, client, client_instructions)

          # Normalize row lengths to match headers safely
          num_cols = len(extracted.column_headers)
          normalized_rows = []
          flagged_notes = []

          for idx, r in enumerate(extracted.rows):
            padded = (r.cells + [""] * num_cols)[:num_cols]
            normalized_rows.append(padded)
            if r.confidence_note:
              flagged_notes.append(f"Row {idx + 1}: {r.confidence_note}")

          df = pd.DataFrame(normalized_rows, columns=extracted.column_headers)
          if deep_clean:
            df = df.drop_duplicates()

          st.session_state["results"].append({
              "filename": f.name,
              "title": extracted.document_title,
              "summary": extracted.summary_notes,
              "df": df,
              "flags": flagged_notes,
          })
        except Exception as e:
          st.error(f"Failed to process `{f.name}`: {e}")

# --- HUMAN-IN-THE-LOOP REVIEW & DOWNLOAD ---
if "results" in st.session_state and st.session_state["results"]:
  st.divider()
  st.subheader("✅ Review, Edit & Export Client Deliverables")

  palette = PALETTES[palette_name]

  for idx, item in enumerate(st.session_state["results"]):
    with st.expander(f"📄 {item['filename']} — {item['title']}", expanded=True):
      if item["flags"]:
        st.warning(
            "**AI Quality Check Flags (Please verify these rows):**\n- "
            + "\n- ".join(item["flags"])
        )

      # Live editable table before export
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
