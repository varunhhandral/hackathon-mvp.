import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Professional Office Data & Sequence Utility", layout="wide"
)

st.title("💼 Professional Office Data Cleaning, Sequencing & Excel Generator")
st.markdown(
    "Upload any raw, scrambled client file. This tool cleans **all rows**,"
    " removes duplicates, **sorts records in proper sequence**, formats dates"
    " as **Day Month Year (Text)**, aligns text and numbers professionally, and"
    " exports a styled multi-sheet Excel report."
)

# 1. File Uploader
uploaded_file = st.file_uploader(
    "Upload Raw Client Dataset (CSV or Excel)", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  try:
    if uploaded_file.name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    else:
      df = pd.read_excel(uploaded_file)
  except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

  st.info(
      f"Loaded **{len(df):,} raw rows** across **{len(df.columns)} columns**."
  )

  # 2. Sequence Preference Selector
  sort_option = st.radio(
      "Choose Sequence Order for Client Deliverable:",
      [
          "ID Sequence (e.g., ZM-0001 → ZM-2000)",
          "Chronological Date Sequence (Oldest → Newest)",
          "Area / Department Grouping + ID Sequence",
      ],
      horizontal=True,
  )

  # 3. One-Click Process Button
  if st.button("🚀 Clean, Arrange Sequence-Wise & Generate Excel"):
    with st.spinner("Cleaning, sorting in sequence, and formatting Excel..."):
      cleaned_df = df.copy()

      # A. Trim whitespace & normalize text casing
      text_cols = cleaned_df.select_dtypes(include=["object"]).columns
      for col in text_cols:
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

      # B. Drop exact duplicates
      before_dups = len(cleaned_df)
      cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)
      dups_removed = before_dups - len(cleaned_df)

      # C. Parse Dates as Day Month Year in Text Format (e.g., 12 September 2026)
      date_col = next(
          (c for c in cleaned_df.columns if "date" in c.lower()), None
      )
      if date_col:
        cleaned_df["_sort_date"] = pd.to_datetime(
            cleaned_df[date_col], errors="coerce"
        )
        cleaned_df[date_col] = cleaned_df["_sort_date"].dt.strftime(
            "%d %B %Y"
        ).fillna("Not Specified")

      # D. Convert word-numbers to digits
      word_map = {
          "One": 1,
          "Two": 2,
          "Three": 3,
          "Four": 4,
          "Five": 5,
          "Six": 6,
      }
      for col in ["Quantity", "Rating"]:
        if col in cleaned_df.columns:
          cleaned_df[col] = cleaned_df[col].replace(word_map)
          cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")
          if col == "Quantity":
            cleaned_df[col] = cleaned_df[col].fillna(1).astype(int)
          else:
            cleaned_df[col] = (
                cleaned_df[col].fillna(cleaned_df[col].median()).round(1)
            )

      # E. Clean Currency & Numeric Columns
      currency_cols = [
          c
          for c in [
              "Item Price",
              "Delivery Fee",
              "Basic Salary",
              "Salary",
              "Price",
          ]
          if c in cleaned_df.columns
      ]
      for col in currency_cols:
        cleaned_df[col] = (
            cleaned_df[col]
            .astype(str)
            .str.replace("Rs.", "", case=False, regex=False)
            .str.replace("Rs", "", case=False, regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce").fillna(
            0
        )

      # F. Clean Attendance & Pincode
      if "Attendance" in cleaned_df.columns:
        cleaned_df["Attendance"] = (
            pd.to_numeric(cleaned_df["Attendance"], errors="coerce")
            .fillna(25)
            .astype(int)
        )
      if "Pincode" in cleaned_df.columns:
        cleaned_df["Pincode"] = (
            pd.to_numeric(cleaned_df["Pincode"], errors="coerce")
            .fillna(0)
            .astype(int)
            .astype(str)
            .replace("0", "Not Provided")
        )

      # Fill remaining missing text values
      for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].fillna("Not Specified")

      # G. Calculated Business Columns
      if all(
          c in cleaned_df.columns
          for c in ["Quantity", "Item Price", "Delivery Fee"]
      ):
        cleaned_df["Total_Revenue"] = (
            cleaned_df["Quantity"] * cleaned_df["Item Price"]
        ) + cleaned_df["Delivery Fee"]

      if all(c in cleaned_df.columns for c in ["Basic Salary", "Attendance"]):
        cleaned_df["Calculated_Salary"] = (
            (cleaned_df["Basic Salary"] / 30.0) * cleaned_df["Attendance"]
        ).round(2)
        cleaned_df["Performance"] = cleaned_df["Attendance"].apply(
            lambda x: "Good" if x >= 25 else "Bad"
        )

      # H. SEQUENCE-WISE SORTING
      id_col = next(
          (
              c
              for c in cleaned_df.columns
              if c.lower() in ["order id", "employee id", "id"]
          ),
          None,
      )
      if id_col:
        cleaned_df["_sort_id_num"] = (
            cleaned_df[id_col]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype(float)
            .fillna(999999)
        )

      if "ID Sequence" in sort_option and id_col:
        cleaned_df = cleaned_df.sort_values(
            by=["_sort_id_num", id_col], ascending=True
        )
      elif "Chronological" in sort_option and date_col:
        sort_cols = ["_sort_date"] + (["_sort_id_num"] if id_col else [])
        cleaned_df = cleaned_df.sort_values(by=sort_cols, ascending=True)
      elif "Area / Department" in sort_option:
        grp = (
            "Area"
            if "Area" in cleaned_df.columns
            else ("Department" if "Department" in cleaned_df.columns else None)
        )
        sort_cols = ([grp] if grp else []) + (
            ["_sort_id_num"] if id_col else []
        )
        if sort_cols:
          cleaned_df = cleaned_df.sort_values(by=sort_cols, ascending=True)

      cleaned_df = cleaned_df.drop(
          columns=[
              c for c in ["_sort_date", "_sort_id_num"] if c in cleaned_df.columns
          ]
      ).reset_index(drop=True)

      # Arrange columns in clean office sequence
      preferred_order = [
          "Order ID",
          "Employee ID",
          "Order Date",
          "Joining Date",
          "Customer Name",
          "Employee Name",
          "Restaurant Name",
          "Area",
          "Department",
          "Pincode",
          "Item",
          "Quantity",
          "Item Price",
          "Delivery Fee",
          "Total_Revenue",
          "Basic Salary",
          "Attendance",
          "Calculated_Salary",
          "Performance",
          "Payment Method",
          "Order Status",
          "Rating",
      ]
      ordered_cols = [c for c in preferred_order if c in cleaned_df.columns]
      remaining_cols = [c for c in cleaned_df.columns if c not in ordered_cols]
      cleaned_df = cleaned_df[ordered_cols + remaining_cols]

      # I. Build Client Summary Sheet
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

      st.session_state["seq_cleaned_df"] = cleaned_df
      st.session_state["seq_summary_df"] = summary_df
      st.session_state["dups_removed"] = dups_removed

  # 4. Display Full Output & Styled Multi-Sheet Excel Export with Proper Alignments
  if "seq_cleaned_df" in st.session_state:
    res_df = st.session_state["seq_cleaned_df"]
    sum_df = st.session_state["seq_summary_df"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sequenced & Cleaned Rows", f"{len(res_df):,}")
    c2.metric("Duplicates Removed", st.session_state["dups_removed"])
    c3.metric("Missing Cells", int(res_df.isnull().sum().sum()))

    from openpyxl.styles import Alignment, Font, PatternFill

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      res_df.to_excel(writer, sheet_name="All_Cleaned_Data", index=False)
      sum_df.to_excel(writer, sheet_name="Client_Summary", index=False)

      header_fill = PatternFill(
          start_color="1E293B", end_color="1E293B", fill_type="solid"
      )
      header_font = Font(color="FFFFFF", bold=True)

      for sheet_name, df_data in [
          ("All_Cleaned_Data", res_df),
          ("Client_Summary", sum_df),
      ]:
        ws = writer.sheets[sheet_name]
        ws.freeze_panes = "A2"

        # Apply correct alignments: Text/Dates left-aligned, Numbers right-aligned
        for col_idx, col_name in enumerate(df_data.columns, 1):
          is_numeric = pd.api.types.is_numeric_dtype(df_data[col_name])
          align_type = "right" if is_numeric else "left"

          for row_idx in range(
              1, len(df_data) + 2
          ):  # Include header row handling
            cell = ws.cell(row=row_idx, column=col_idx)
            if row_idx == 1:
              cell.fill = header_fill
              cell.font = header_font
              cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
              cell.alignment = Alignment(
                  horizontal=align_type, vertical="center"
              )

        # Auto-adjust column widths
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
            f"📥 Download Sequenced & Formatted Excel ({len(res_df):,} Rows +"
            " Summary)"
        ),
        data=output.getvalue(),
        file_name="Client_Sequenced_Cleaned_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.subheader("📊 Client Summary Table")
    st.dataframe(sum_df, use_container_width=True)

    st.subheader(
        f"✨ Sequence-Ordered & Cleaned Dataset (All {len(res_df):,} Rows)"
    )
    st.dataframe(res_df, use_container_width=True, height=500)
              
