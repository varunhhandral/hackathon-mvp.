import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Professional Office Data Entry & Cleaning Utility",
    layout="wide",
)

st.title("💼 Professional Office Data Entry & Cleaning Assistant")
st.markdown(
    "Upload any raw office report or client dataset. This app automatically"
    " standardizes text, formats dates, cleans currency/numbers, computes"
    " attendance-based salaries, applies performance rules, removes duplicates,"
    " and generates a client-ready multi-sheet Excel report!"
)

# 1. File Uploader
uploaded_file = st.file_uploader(
    "Upload Raw Dataset (CSV or Excel)", type=["csv", "xlsx"]
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

  st.subheader("📋 Raw Data Preview")
  st.dataframe(df.head(5), use_container_width=True)

  # 2. Automated Office Formatting & Processing Button
  if st.button("🚀 Run Professional Office Formatting & Calculations"):
    with st.spinner(
        "Standardizing text, formatting dates, calculating salaries, and"
        " evaluating performance..."
    ):
      cleaned_df = df.copy()

      # A. Remove Duplicates automatically (as covered in professional workflow)
      cleaned_df = cleaned_df.drop_duplicates()

      # B. Standardize Text Casing & Whitespace
      text_cols = [
          col
          for col in [
              "Employee Name",
              "Department",
              "Area",
              "Restaurant Name",
              "Customer Name",
              "Item",
              "Payment Method",
              "Order Status",
          ]
          if col in cleaned_df.columns
      ]
      for col in text_cols:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip().str.title()

      # C. Format Joining / Order Dates cleanly
      date_cols = [
          col for col in ["Joining Date", "Order Date"] if col in cleaned_df.columns
      ]
      for col in date_cols:
        cleaned_df[col] = pd.to_datetime(
            cleaned_df[col], errors="coerce"
        ).dt.strftime("%B %d, %Y")

      # D. Clean Numeric & Currency Columns (Remove symbols like ₹, Rs., commas)
      for col in ["Basic Salary", "Salary", "Item Price", "Delivery Fee"]:
        if col in cleaned_df.columns:
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

      # E. Clean Attendance & Append ' Days' Suffix for presentation
      if "Attendance" in cleaned_df.columns:
        cleaned_df["Attendance"] = (
            pd.to_numeric(cleaned_df["Attendance"], errors="coerce")
            .fillna(25)
            .astype(int)
        )

      # F. Salary Calculation Proportional to Attendance (Basic Salary / 30 * Attendance)
      if "Basic Salary" in cleaned_df.columns and "Attendance" in cleaned_df.columns:
        cleaned_df["Calculated Salary"] = (
            (cleaned_df["Basic Salary"] / 30.0) * cleaned_df["Attendance"]
        ).round(2)

      # G. Performance Condition (IF Attendance >= 25 -> Good, else Bad)
      if "Attendance" in cleaned_df.columns:
        cleaned_df["Performance"] = cleaned_df["Attendance"].apply(
            lambda x: "Good" if x >= 25 else "Bad"
        )

      # H. Generate Summary Report (Area-wise or Department-wise totals)
      group_col = (
          "Area"
          if "Area" in cleaned_df.columns
          else ("Department" if "Department" in cleaned_df.columns else None)
      )
      if group_col and "Calculated Salary" in cleaned_df.columns:
        summary_df = (
            cleaned_df.groupby(group_col)
            .agg(
                Total_Records=(cleaned_df.columns[0], "count"),
                Total_Payout_Salary=("Calculated Salary", "sum"),
            )
            .reset_index()
        )
      elif group_col:
        summary_df = (
            cleaned_df.groupby(group_col)
            .agg(Total_Records=(cleaned_df.columns[0], "count"))
            .reset_index()
        )
      else:
        summary_df = pd.DataFrame(columns=["Summary", "Total_Count"])

      # Store in session state
      st.session_state["office_cleaned_df"] = cleaned_df
      st.session_state["office_summary_df"] = summary_df

    st.success(
        "Professional formatting, duplicate removal, salary calculations, and"
        " performance flags applied successfully!"
    )

  # 3. Display Results & One-Click Download
  if "office_cleaned_df" in st.session_state:
    st.markdown("---")
    st.subheader("✨ Cleaned & Formatted Data Preview")
    st.dataframe(
        st.session_state["office_cleaned_df"].head(10), use_container_width=True
    )

    st.subheader("📊 Summary Deliverable Report")
    st.dataframe(st.session_state["office_summary_df"], use_container_width=True)

    # 4. Multi-Sheet Excel Export
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      st.session_state["office_cleaned_df"].to_excel(
          writer, sheet_name="Cleaned_Office_Data", index=False
      )
      st.session_state["office_summary_df"].to_excel(
          writer, sheet_name="Summary_Report", index=False
      )
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Complete Multi-Sheet Excel Report for Client",
        data=excel_data,
        file_name="Professional_Office_Data_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
  st.info("👈 Upload your messy client CSV or Excel file above to begin.")
    
