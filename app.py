import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Professional Office Data Entry & Cleaning Utility",
    layout="wide",
)

st.title("💼 One-Click Data Cleaning & Client Deliverable Generator")
st.markdown(
    "Upload any raw client file. This tool cleans **every single row**, removes"
    " duplicates, standardizes dates and text, calculates totals, and exports a"
    " complete multi-sheet Excel file."
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

  # 2. One-Click Full Cleaning & Calculation Button
  if st.button("🚀 Clean All Data & Generate Client Excel"):
    with st.spinner("Cleaning all rows and building summary sheets..."):
      cleaned_df = df.copy()

      # A. Trim whitespace & normalize casing across all text columns
      text_cols = cleaned_df.select_dtypes(include=["object"]).columns
      for col in text_cols:
        # Leave Order IDs uppercase, Title Case everything else
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
        # Replace string 'Nan' or 'None' back to actual NaN before filling
        cleaned_df[col] = cleaned_df[col].replace(
            ["Nan", "None", "NAT", ""], pd.NA
        )

      # B. Drop exact duplicate rows
      before_dups = len(cleaned_df)
      cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)
      dups_removed = before_dups - len(cleaned_df)

      # C. Standardize Date Columns
      for col in cleaned_df.columns:
        if "date" in col.lower():
          parsed_dates = pd.to_datetime(cleaned_df[col], errors="coerce")
          cleaned_df[col] = parsed_dates.dt.strftime("%B %d, %Y").fillna(
              "Not Specified"
          )

      # D. Convert word-numbers to digits (Quantity & Rating)
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
            cleaned_df[col] = cleaned_df[col].fillna(
                cleaned_df[col].median()
            ).round(1)

      # E. Clean Currency & Numeric Columns (₹, Rs., commas)
      currency_cols = [
          col
          for col in [
              "Item Price",
              "Delivery Fee",
              "Basic Salary",
              "Salary",
              "Price",
          ]
          if col in cleaned_df.columns
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

      # F. Clean Attendance & Pincode if present
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

      # Fill remaining missing text values cleanly
      for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].fillna("Not Specified")

      # G. Calculated Columns (Revenue & Office Payroll/Performance)
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

      # H. Build Client Summary Sheet (Area-wise or Department-wise)
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

      st.session_state["full_cleaned_df"] = cleaned_df
      st.session_state["full_summary_df"] = summary_df
      st.session_state["dups_removed"] = dups_removed

  # 3. Show Full Output & One-Click Excel Download
  if "full_cleaned_df" in st.session_state:
    res_df = st.session_state["full_cleaned_df"]
    sum_df = st.session_state["full_summary_df"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Cleaned Rows Ready", f"{len(res_df):,}")
    c2.metric("Duplicates Removed", st.session_state["dups_removed"])
    c3.metric("Remaining Missing Cells", int(res_df.isnull().sum().sum()))

    # One-Click Download at the top so you don't even have to scroll
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      res_df.to_excel(writer, sheet_name="All_Cleaned_Data", index=False)
      sum_df.to_excel(writer, sheet_name="Client_Summary", index=False)

    st.download_button(
        label=(
            f"📥 Download Complete Cleaned Excel ({len(res_df):,} Rows +"
            " Summary)"
        ),
        data=output.getvalue(),
        file_name="Client_Fully_Cleaned_Deliverable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.subheader("📊 Client Summary Table")
    st.dataframe(sum_df, use_container_width=True)

    st.subheader(f"✨ Complete Cleaned Dataset (All {len(res_df):,} Rows)")
    # Displays the entire cleaned dataframe in a scrollable table
    st.dataframe(res_df, use_container_width=True, height=500)
        
