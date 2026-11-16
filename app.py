import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Student Performance Insights", layout="centered")

# Vibrant Custom CSS Theme
st.markdown("""
<style>
.hero {background: linear-gradient(135deg, #6366f1 0%, #ec4899 50%, #f59e0b 100%); padding: 22px; border-radius: 16px; color: white; margin-bottom: 18px; box-shadow: 0 8px 20px rgba(99,102,241,0.25);}
.hero h1 {margin: 0; font-size: 2rem; color: white;}
.hero p {margin: 6px 0 0; opacity: 0.95; font-size: 0.98rem;}
div[data-testid="stMetric"] {background: linear-gradient(135deg, #f8fafc, #eef2ff); border-left: 5px solid #6366f1; padding: 12px 16px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);}
div.stButton > button {background: linear-gradient(90deg, #4f46e5, #db2777); color: white; border: none; border-radius: 10px; font-weight: 600; padding: 0.55rem 1.2rem;}
div.stDownloadButton > button {background: linear-gradient(90deg, #059669, #0284c7); color: white; border: none; border-radius: 10px; font-weight: 600;}
</style>
<div class="hero">
  <h1>Student Performance Insights</h1>
  <p>RNSIT / VTU Integrated Scheme: CIE (50) [Theory + Lab] + SEE (50) [Theory + External Lab] = Total (100), SGPA & CGPA</p>
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
              "At Risk": "background-color:#fee2e2;color:#991b1b;font-weight:bold", "On Track": "background-color:#dcfce7;color:#166534;font-weight:bold"}
    return colors.get(val, "")

np.random.seed(42)
n = 300
att = np.random.randint(55, 100, n)
cie = np.random.uniform(18, 50, n)
sem_ex = np.random.randint(35, 98, n)
tot_y = np.clip(cie + (sem_ex * 0.45) + (att * 0.05) + np.random.normal(0, 1.5, n), 0, 100)

cols = ["Attendance (%)", "CIE Marks (/50)", "This Sem Exam (/100)"]
df = pd.DataFrame({cols[0]: att, cols[1]: cie, cols[2]: sem_ex, "Total": tot_y})
X_tr, X_te, y_tr, y_te = train_test_split(df[cols], df["Total"], test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_tr, y_tr)
preds = model.predict(X_te)

st.subheader("Model Performance & Key Drivers")
c1, c2 = st.columns(2)
c1.metric("Total Score MAE", f"{mean_absolute_error(y_te, preds):.2f} / 100")
c2.metric("R2 Accuracy", f"{r2_score(y_te, preds):.2f}")
imp = pd.DataFrame({"Factor": cols, "Impact": model.feature_importances_}).sort_values("Impact")
st.bar_chart(imp.set_index("Factor"), color="#ec4899")
st.divider()

st.subheader("6-Subject Semester Evaluation & CGPA (RNSIT Scheme)")
g1, g2 = st.columns(2)
curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, 7.65, 0.05)
comp_sems = g2.number_input("Completed Semesters", 1, 8, 3, 1)

subs_init = [
    ("Data Structures", 4, 86, 41, 43, 5, 4, 78, True, 44, 46, True, 42),
    ("Operating Systems", 4, 74, 26, 28, 4, 3, 64, True, 38, 40, False, 0),
    ("Database Systems", 4, 90, 44, 46, 5, 5, 84, True, 45, 48, True, 44),
    ("Computer Networks", 3, 70, 22, 24, 3, 3, 58, False, 0, 0, False, 0),
    ("Discrete Maths", 4, 82, 36, 38, 4, 5, 74, False, 0, 0, False, 0),
    ("Software Engg", 3, 92, 45, 47, 5, 5, 86, False, 0, 0, False, 0)
]

rows = []
for i, (nm, cr, at, i1, i2, a1, a2, ts, h_lab, li1, li2, h_ext, ext_m) in enumerate(subs_init):
    with st.expander(f"Subject {i+1}: {nm}", expanded=(i == 0)):
        c_a, c_b = st.columns([3, 1])
        s_nm = c_a.text_input("Subject Name (Editable)", nm, key=f"n{i}")
        s_cr = c_b.number_input("Credits", 1, 6, cr, key=f"c{i}")
        c_c, c_d = st.columns(2)
        s_at = c_c.slider("Attendance (%)", 40, 100, at, key=f"a{i}")
        s_ts = c_d.number_input("This Sem Exam Final (/100)", 0, 100, ts, key=f"ts{i}")
        k1, k2, k3, k4 = st.columns(4)
        v1 = k1.number_input("Theory Int 1 (/50)", 0, 50, i1, key=f"i1{i}")
        v2 = k2.number_input("Theory Int 2 (/50)", 0, 50, i2, key=f"i2{i}")
        v3 = k3.number_input("Assign 1 (/5)", 0, 5, a1, key=f"a1{i}")
        v4 = k4.number_input("Assign 2 (/5)", 0, 5, a2, key=f"a2{i}")
        has_lab = st.checkbox("Include Lab Component for this Subject?", value=h_lab, key=f"hl{i}")
        if has_lab:
            l1, l2, l3 = st.columns(3)
            lv1 = l1.number_input("Lab Int 1 (/50)", 0, 50, li1, key=f"li1{i}")
            lv2 = l2.number_input("Lab Int 2 (/50)", 0, 50, li2, key=f"li2{i}")
            has_ext = l3.checkbox("External Lab Exam?", value=h_ext, key=f"he{i}")
            ext_val = st.number_input("External Lab Marks (/50)", 0, 50, ext_m if ext_m > 0 else 40, key=f"ex{i}") if has_ext else 0
            cie_val = round(((v1 + v2) / 100.0) * 25.0 + ((v3 + v4) / 10.0) * 5.0 + ((lv1 + lv2) / 100.0) * 20.0, 1)
            
