import streamlit as st
import pandas as pd
from google import genai

st.title("🚀 Hackathon Data Science MVP")
st.write("Welcome! This app runs on Python, Streamlit, and Gemini.")

# File upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview:")
    st.dataframe(df.head())
    
    st.subheader("Quick Chart:")
    st.bar_chart(df.select_dtypes(include=['number']))
    
    # AI Insights Section
    st.subheader("🤖 Gemini AI Insights")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    if api_key and st.button("Generate AI Analysis"):
        with st.spinner("Analyzing dataset..."):
            client = genai.Client(api_key=api_key)
            csv_summary = df.describe().to_string()
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Analyze this dataset summary and give 3 key actionable insights for a hackathon presentation:\n{csv_summary}"
            )
            st.success("Analysis Complete!")
            st.write(response.text)
else:
    st.info("👆 Upload a dataset above to see the magic happen.")
    
