import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zomato Data Cleaning & Freelance Utility", layout="wide"
)

st.title("⚡ One-Click Zomato Data Cleaning & Area-Wise Summary Utility")
st.markdown(
    "Upload any raw, messy Zomato order report. This tool instantly standardizes"
    " text, calculates total revenue per order, generates area-wise summary"
    " tables, and gives you a clean Excel file ready to send to clients!"
)

# 1. File Uploader
uploaded_file = st.file_uploader(
    "Upload Raw Client Report (CSV or Excel)", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  # Read file depending on extension
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

  # 2. Automated Cleaning & Calculation Button
  if st.button("🚀 Process, Clean & Generate Client Deliverable"):
    with st.spinner("Cleaning columns, fixing text, and calculating revenue..."):
      cleaned_df = df.copy()

      # Normalize text columns if they exist
      text_cols = [
          "Restaurant Name",
          "Customer Name",
          "Area",
          "Item",
          "Payment Method",
          "Order Status",
      ]
      for col in text_cols:
        if col in cleaned_df.columns:
          cleaned_df[col] = (
              cleaned_df[col].astype(str).str.strip().str.title()
          )

      # Clean numeric columns (Quantity, Item Price, Delivery Fee)
      if "Quantity" in cleaned_df.columns:
        # Handle word quantities like 'two' or 'five' if present
        word_to_num = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
        }
        cleaned_df["Quantity"] = cleaned_df["Quantity"].replace(word_to_num)
        cleaned_df["Quantity"] = (
            pd.to_numeric(cleaned_df["Quantity"], errors="coerce").fillna(1).astype(int)
        )

      for price_col in ["Item Price", "Delivery Fee"]:
        if price_col in cleaned_df.columns:
          cleaned_df[price_col] = (
              cleaned_df[price_col]
              .astype(str)
              .str.replace("Rs.", "", case=False, regex=False)
              .str.replace("₹", "", regex=False)
              .str.strip()
          )
          cleaned_df[price_col] = pd.to_numeric(
              cleaned_df[price_col], errors="coerce"
          ).fillna(0)

      # Calculate Total Revenue per order = (Quantity * Item Price) + Delivery Fee
      if (
          "Quantity" in cleaned_df.columns
          and "Item Price" in cleaned_df.columns
          and "Delivery Fee" in cleaned_df.columns
      ):
        cleaned_df["Total_Revenue"] = (
            cleaned_df["Quantity"] * cleaned_df["Item Price"]
        ) + cleaned_df["Delivery Fee"]
      else:
        cleaned_df["Total_Revenue"] = 0

      # Create Area-wise Summary Table
      if "Area" in cleaned_df.columns:
        area_summary = (
            cleaned_df.groupby("Area")
            .agg(
                Total_Orders=("Order ID", "count"),
                Total_Revenue=("Total_Revenue", "sum"),
            )
            .reset_index()
        )
      else:
        area_summary = pd.DataFrame(
            columns=["Area", "Total_Orders", "Total_Revenue"]
        )

      # Store in session state for downloading
      st.session_state["cleaned_df"] = cleaned_df
      st.session_state["area_summary"] = area_summary

    st.success("Data cleaned and summaries generated successfully!")

  # 3. Display Results if processed
  if "cleaned_df" in st.session_state:
    st.markdown("---")
    st.subheader("✨ Cleaned Zomato Report Preview")
    st.dataframe(st.session_state["cleaned_df"].head(10), use_container_width=True)

    st.subheader("📊 Area-Wise Summary Deliverable")
    st.dataframe(st.session_state["area_summary"], use_container_width=True)

    # 4. One-Click Multi-Sheet Excel Export
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      st.session_state["cleaned_df"].to_excel(
          writer, sheet_name="Cleaned_Zomato_Data", index=False
      )
      st.session_state["area_summary"].to_excel(
          writer, sheet_name="Area_Wise_Summary", index=False
      )
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Complete Excel Report for Client",
        data=excel_data,
        file_name="TastyBites_Zomato_Cleaned_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
  st.info(
      "👈 Upload your client's messy CSV or Excel file above to get started."
      )
    
