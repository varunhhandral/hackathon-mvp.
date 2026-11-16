import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="One-Click Data Entry & Cleaning Utility", layout="wide"
)
st.title("⚡ One-Click Data Cleaning & Entry Assistant")

# 1. File Upload
uploaded_file = st.file_uploader(
    "Upload Raw Client CSV or Excel File", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  else:
    df = pd.read_excel(uploaded_file)

  st.subheader("Raw Data Preview")
  st.dataframe(df.head(5), use_container_width=True)

  # 2. One-Click Cleaning Actions
  st.subheader("🛠️ One-Click Cleaning Operations")
  col1, col2, col3 = st.columns(3)

  if col1.button("Trim Whitespaces & Capitalise Text"):
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
      df[col] = df[col].astype(str).str.strip().str.title()
    st.success("Successfully cleaned text spacing and casing!")

  if col2.button("Fill Missing Numeric Values"):
    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    st.success("Successfully filled missing numbers with column medians!")

  if col3.button("Drop Duplicate Rows"):
    before_len = len(df)
    df = df.drop_duplicates()
    dropped = before_len - len(df)
    st.success(f"Removed {dropped} duplicate rows!")

  # 3. Manual Data Entry Section
  with st.expander("➕ Add New Record Manually"):
    with st.form("entry_form"):
      new_row = {}
      form_cols = st.columns(min(3, len(df.columns)))
      for idx, col in enumerate(df.columns):
        with form_cols[idx % len(form_cols)]:
          new_row[col] = st.text_input(f"Enter {col}")

      submit_entry = st.form_submit_button("Append Record")
      if submit_entry:
        # Convert types or append
        new_df_row = pd.DataFrame([new_row])
        df = pd.concat([df, new_df_row], ignore_index=True)
        st.success("New record added successfully!")

  # 4. Cleaned Data Preview & Export
  st.subheader("✅ Cleaned Dataset Output")
  st.dataframe(df.head(10), use_container_width=True)

  # Export button
  csv_data = df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Cleaned CSV File",
      data=csv_data,
      file_name="cleaned_client_data.csv",
      mime="text/csv",
  )
else:
  st.info("Upload a dataset above to start cleaning.")
  
