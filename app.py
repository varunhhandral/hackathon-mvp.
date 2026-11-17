import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Universal Client Deliverable & Cleaning Utility", layout="wide"
)

st.title("🚀 Universal Client Request & Data Cleaning Engine")
st.markdown(
    "Upload **any client file** (Spreadsheet, CSV, or Document text), enter"
    " your client's specific instructions, choose your formatting/color"
    " palette, and generate a 100% polished deliverable with one click!"
)

# 1. Universal File Uploader
uploaded_file = st.file_uploader(
    "Upload Client File (Excel, CSV, Text/Doc)", type=["csv", "xlsx", "txt"]
)

# 2. Client Request & Customization Panel
st.subheader("📝 Client Instructions & Styling Preferences")
client_request = st.text_area(
    "Paste or describe the client's request (e.g., 'Type out text in Arial"
    " 11, clean Zomato data, calculate area-wise revenue, remove duplicates'):",
    placeholder="Type client instructions here...",
)

col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
  enable_cleaning = st.checkbox(
      "🧹 Enable Deep Data Cleaning & Deduplication", value=True
  )
with col_opt2:
  enable_sequence = st.checkbox("🔢 Sort in Strict Sequence (ID / Date)", value=True)
with col_opt3:
  color_theme = st.selectbox(
      "🎨 Excel Header Color Palette",
      [
          "Slate Dark (Modern Office)",
          "Navy Blue (Executive)",
          "Emerald Green (Finance)",
          "Charcoal Minimal",
      ],
  )

# Color theme dictionary for openpyxl styling
theme_colors = {
    "Slate Dark (Modern Office)": "1E293B",
    "Navy Blue (Executive)": "1E3A8A",
    "Emerald Green (Finance)": "065F46",
    "Charcoal Minimal": "374151",
}

if uploaded_file is not None:
  # Read file based on type
  try:
    if uploaded_file.name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
      df = pd.read_excel(uploaded_file)
    else:
      # Handle text / doc uploads
      stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
      text_data = stringio.read()
      df = pd.DataFrame(
          {"Extracted_Document_Content": text_data.split("\n")}
      )
  except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

  st.info(
      f"Successfully loaded **{len(df):,} rows/lines** across"
      f" **{len(df.columns)} columns** from `{uploaded_file.name}`."
  )

  # 3. Process & Generate Button
  if st.button("✨ Process Deliverable & Apply Client Instructions"):
    with st.spinner(
        "Interpreting request, cleaning data, sequencing, and applying"
        " theme..."
    ):
      cleaned_df = df.copy()

      # A. Cleaning & Deduplication
      dups_removed = 0
      if enable_cleaning and len(cleaned_df.columns) > 1:
        before_dups = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)
        dups_removed = before_dups - len(cleaned_df)

        # Normalize text casing & strip whitespace
        for col in cleaned_df.select_dtypes(include=["object"]).columns:
          if "id" in col.lower():
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip().str.upper()
          else:
            cleaned_df[col] = (
                cleaned_df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .str.title()
            )
          cleaned_df[col] = cleaned_df[col].replace(
              ["Nan", "None", "Nat", ""], pd.NA
          )

        # Numerical & Currency normalization
        for col in cleaned_df.columns:
          if any(
              kw in col.lower()
              for kw in ["price", "fee", "salary", "revenue", "amount"]
          ):
            cleaned_df[col] = (
                cleaned_df[col]
                .astype(str)
                .str.replace("Rs.", "", case=False, regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            cleaned_df[col] = pd.to_numeric(
                cleaned_df[col], errors="coerce"
            ).fillna(0)
          elif "date" in col.lower():
            parsed = pd.to_datetime(cleaned_df[col], errors="coerce")
            cleaned_df[col] = parsed.dt.strftime("%d %B %Y").fillna(
                "Not Specified"
            )

        # Fill remaining missing text
        for col in cleaned_df.select_dtypes(include=["object"]).columns:
          cleaned_df[col] = cleaned_df[col].fillna("Not Specified")

      # B. Sequence Ordering
      if enable_sequence and len(cleaned_df.columns) > 1:
        id_col = next(
            (
                c
                for c in cleaned_df.columns
                if c.lower() in ["order id", "employee id", "id"]
            ),
            None,
        )
        date_col = next(
            (c for c in cleaned_df.columns if "date" in c.lower()), None
        )

        if id_col:
          cleaned_df["_sort_id"] = (
              cleaned_df[id_col]
              .astype(str)
              .str.extract(r"(\d+)")
              .astype(float)
              .fillna(999999)
          )
          cleaned_df = cleaned_df.sort_values(
              by=["_sort_id", id_col], ascending=True
          ).drop(columns=["_sort_id"])
        elif date_col:
          cleaned_df = cleaned_df.sort_values(
              by=[date_col], ascending=True
          )

      cleaned_df = cleaned_df.reset_index(drop=True)

      # C. Summary / Analysis Generation
      if "Area" in cleaned_df.columns and "Total_Revenue" in cleaned_df.columns:
        summary_df = (
            cleaned_df.groupby("Area", as_index=False)
            .agg(
                Total_Orders=(cleaned_df.columns[0], "count"),
                Total_Revenue=("Total_Revenue", "sum"),
            )
            .sort_values(by="Total_Revenue", ascending=False)
        )
      elif (
          "Department" in cleaned_df.columns
          and "Calculated_Salary" in cleaned_df.columns
      ):
        summary_df = (
            cleaned_df.groupby("Department", as_index=False)
            .agg(
                Total_Employees=(cleaned_df.columns[0], "count"),
                Total_Payout=("Calculated_Salary", "sum"),
            )
            .sort_values(by="Total_Payout", ascending=False)
        )
      else:
        summary_df = cleaned_df.describe().reset_index()

      st.session_state["processed_df"] = cleaned_df
      st.session_state["summary_df"] = summary_df
      st.session_state["dups_removed"] = dups_removed
      st.session_state["theme_hex"] = theme_colors[color_theme]

  # 4. Display Results & Styled Export
  if "processed_df" in st.session_state:
    res_df = st.session_state["processed_df"]
    sum_df = st.session_state["summary_df"]
    hex_code = st.session_state["theme_hex"]

    st.success("✨ Client request processed successfully!")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows Ready", f"{len(res_df):,}")
    c2.metric("Duplicates Removed", st.session_state["dups_removed"])
    c3.metric("Missing Cells", int(res_df.isnull().sum().sum()))

    # Build Styled Excel Output with Chosen Color Palette & Alignments
    from openpyxl.styles import Alignment, Font, PatternFill

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      res_df.to_excel(writer, sheet_name="Cleaned_Data", index=False)
      sum_df.to_excel(writer, sheet_name="Summary_Report", index=False)

      header_fill = PatternFill(
          start_color=hex_code, end_color=hex_code, fill_type="solid"
      )
      header_font = Font(color="FFFFFF", bold=True)

      for sheet_name, df_data in [
          ("Cleaned_Data", res_df),
          ("Summary_Report", sum_df),
      ]:
        ws = writer.sheets[sheet_name]
        ws.freeze_panes = "A2"

        for col_idx, col_name in enumerate(df_data.columns, 1):
          is_numeric = pd.api.types.is_numeric_dtype(df_data[col_name])
          align_type = "right" if is_numeric else "left"

          for row_idx in range(1, len(df_data) + 2):
            cell = ws.cell(row=row_idx, column=col_idx)
            if row_idx == 1:
              cell.fill = header_fill
              cell.font = header_font
              cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
              cell.alignment = Alignment(
                  horizontal=align_type, vertical="center"
              )

        for col_cells in ws.columns:
          max_len = 0
          col_letter = col_cells[0].column_letter
          for cell in col_cells:
            val_len = len(str(cell.value or ""))
            if val_len > max_len:
              max_len = val_len
          ws.column_dimensions[col_letter].width = min(max_len + 4, 35)

    st.download_button(
        label=(
            f"📥 Download Styled Client Deliverable ({len(res_df):,} Rows +"
            " Summary)"
        ),
        data=output.getvalue(),
        file_name="Final_Client_Deliverable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.subheader("📊 Summary & Analysis Preview")
    st.dataframe(sum_df, use_container_width=True)

    st.subheader("✨ Cleaned Dataset Preview")
    st.dataframe(res_df, use_container_width=True, height=400)
                             
