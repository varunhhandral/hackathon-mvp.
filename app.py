import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Student Performance Insights", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Plus Jakarta Sans', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #eef2ff 0%, #fdf2f8 45%, #f0fdf4 100%);}
.hero {background: linear-gradient(125deg, #312e81 0%, #6d28d9 45%, #db2777 100%); padding: 28px 26px; border-radius: 20px; color: white; margin-bottom: 22px; box-shadow: 0 14px 32px rgba(109,40,217,0.22); border: 1px solid rgba(255,255,255,0.2);}
.hero h1 {margin: 0; font-size: 2.05rem; font-weight: 800; letter-spacing: -0.5px; color: white;}
.hero p {margin: 8px 0 0; opacity: 0.92; font-size: 0.96rem; line-height: 1.45;}
.pill-row {display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;}
.pill {background: rgba(255,255,255,0.16); backdrop-filter: blur(6px); padding: 4px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 600;}
div[data-testid="stMetric"] {background: rgba(255,255,255,0.88); border: 1px solid #e0e7ff; border-top: 4px solid #7c3aed; padding: 14px 16px; border-radius: 16px; box-shadow: 0 6px 18px rgba(15,23,42,0.05);}
div[data-testid="stExpander"] {background: rgba(255,255,255,0.92); border-radius: 16px; border: 1.5px solid #ddd6fe; box-shadow: 0 6px 16px rgba(109,40,217,0.06); margin-bottom: 10px; overflow: hidden;}
div[data-testid="stExpander"] summary {background: linear-gradient(90deg, #f5f3ff, #fdf2f8); padding: 10px 14px; font-weight: 700; color: #312e81;}
div[data-baseweb="input"], div[data-baseweb="base-input"] {background: linear-gradient(135deg, #f5f3ff 0%, #fdf4ff 100%) !important; border: 1.5px solid #c4b5fd !important; border-radius: 11px !important; transition: all 0.2s ease;}
div[data-baseweb="input"]:focus-within, div[data-baseweb="base-input"]:focus-within {border-color: #db2777 !important; box-shadow: 0 0 0 3px rgba(219,39,119,0.18) !important; background: #ffffff !important;}
div[data-baseweb="input"] input {color: #1e1b4b !important; font-weight: 600 !important;}
button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {background-color: #ede9fe !important; color: #5b21b6 !important; border-radius: 8px !important; margin: 2px !important;}
button[data-testid="stNumberInputStepDown"]:hover, button[data-testid="stNumberInputStepUp"]:hover {background-color: #7c3aed !important; color: white !important;}
div[data-testid="stFileUploaderDropzone"] {background: linear-gradient(135deg, #eef2ff, #fce7f3) !important; border: 2px dashed #a855f7 !important; border-radius: 16px !important;}
div[data-baseweb="select"] > div {background: linear-gradient(135deg, #f5f3ff, #fdf4ff) !important; border: 1.5px solid #c4b5fd !important; border-radius: 11px !important;}
div.stButton > button {background: linear-gradient(90deg, #4f46e5, #9333ea, #db2777); color: white; border: none; border-radius: 999px; font-weight: 700; padding: 0.6rem 1.6rem; box-shadow: 0 6px 16px rgba(147,51,234,0.28); width: 100%;}
div.stDownloadButton > button {background: linear-gradient(90deg, #0d9488, #0284c7); color: white; border: none; border-radius: 999px; font-weight: 600; padding: 0.5rem 1.4rem;}
.score-badge {background: linear-gradient(90deg, #eef2ff, #fae8ff); border-left: 4px solid #8b5cf6; padding: 10px 14px; border-radius: 10px; font-weight: 700; color: #1e1b4b; font-size: 0.9rem; margin-top: 6px;}
</style>
<div class="hero">
  <h1>Student Performance Insights</h1>
  <p>AI-Powered RNSIT & VTU Academic Analytics, Integrated CIE + SEE Evaluator & Mentor Co-Pilot</p>
  <div class="pill-row">
    <span class="pill">CIE (50) + SEE (50) = 100</span>
    <span class="pill">Theory + Lab Scaling</span>
    <span class="pill">Credit-Weighted SGPA & CGPA</span>
    <span class="pill">1,000-Student Batch Engine</span>
  </div>
</div>
""", unsafe_allow_html=True)

def get_grade(tot, cie, see):
    if cie < 20 or see < 18 or tot < 40: return 0.0, "F"
    if tot >= 90: return 10.0, "O"
    if tot >= 80: return 9.0, "A+"
    if tot >= 70: return 8.0, "A"
    if tot >= 60: return 7.0, "B+"
    if tot >= 55: return 6.0, "B"
    if tot >= 50: return 5.0, "C"
    return 4.0, "P"

def style_grade(val):
    colors = {"O": "background-color:#dcfce7;color:#166534;font-weight:bold", "A+": "background-color:#d1fae5;color:#065f46;font-weight:bold",
              "A": "background-color:#dbeafe;color:#1e40af;font-weight:bold", "B+": "background-color:#e0e7ff;color:#3730a3",
              "B": "background-color:#fef3c7;color:#92400e", "C": "background-color:#ffedd5;color:#9a3412",
              "P": "background-color:#f3f4f6;color:#374151", "F": "background-color:#fee2e2;color:#991b1b;font-weight:bold",
              "At Risk": "background-color:#fee2e2;color:#991b1b;font-weight:bold", "On Track": "background-color:#dcfce7;color:#166534;font-weight:bold
