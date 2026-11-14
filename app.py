import streamlit as st
import pandas as pd

st.title("🚀 Hackathon Data Science MVP")
st.write("Welcome! This app runs on Python and Streamlit.")

# Upload file section
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview:")
    st.dataframe(df.head())
    
    st.subheader("Quick Chart:")
    st.bar_chart(df.select_dtypes(include=['number']))
else:
    st.info("👆 Upload a dataset above to see the magic happen.")
  
