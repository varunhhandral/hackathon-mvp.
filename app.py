import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("RNSIT / VTU Scheme: **CIE (50)** [2 Internals + 2 Assignments] + **Predicted SEE (50)** = **Total (100)**, SGPA & CGPA.")

def get_grade(tot, cie, see):
    if cie < 20 or see < 18 or tot < 40: return 0.0, "F"
    if tot >= 90: return 10.0, "O"
    if tot >= 80: return 9.0, "A+"
    if tot >= 70: return 8.0, "A"
    if tot >= 60: return 7.0, "B+"
    if tot >= 55: return 6.0, "B"
    if tot >= 50: return 5.0, "C"
    return 4.0, "P"

np.random.seed(42)
n = 300
att = np.random.randint(55, 100, n)
cie = np.random.uniform(18, 50, n)
last_sem = np.random.randint(35, 98, n)
see = np.clip(0.45 * cie + 0.18 * last_sem + 0.12 * att + np.random.normal(0, 2.2, n), 0, 50)

cols = ["Attendance (%)", "CIE Marks (/50)", "Last Sem Exam (/100)"]
df = pd.DataFrame({cols[0]: att, cols[1]: cie, cols[2]: last_sem, "SEE": see})
X_tr, X_te, y_tr, y_te = train_test_split(df[cols], df["SEE"], test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_tr, y_tr)
preds = model.predict(X_te)

st.subheader("Model Performance & Key Drivers")
c1, c2 = st.columns(2)
c1.metric("SEE MAE Error", f"{mean_absolute_error(y_te, preds):.2f} / 50")
c2.metric("R2 Accuracy", f"{r2_score(y_te, preds):.2f}")
imp = pd.DataFrame({"Factor": cols, "Impact": model.feature_importances_}).sort_values("Impact")
st.bar_chart(imp.set_index("Factor"))
st.divider()

st.subheader("6-Subject Semester Simulator (RNSIT Scheme)")
g1, g2 = st.columns(2)
curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, 7.65, 0.05)
comp_sems = g2.number_input("Completed Semesters", 1, 8, 3, 1)

subs_init = [
    ("Data Structures", 4, 86, 41, 43, 5, 4, 78),
    ("Operating Systems", 4, 72, 24, 26, 4, 3, 62),
    ("Database Systems", 4, 90, 44, 46, 5, 5, 84),
    ("Computer Networks", 3, 68, 18, 20, 3, 3, 54),
    ("Discrete Maths", 4, 80, 36, 38, 4, 5, 72),
    ("Software Engg", 3, 92, 45, 47, 5, 5, 86)
]

rows = []
for i, (nm, cr, at, i1, i2, a1, a2, ls) in enumerate(subs_init):
    with st.expander(f"Subject {i+1}: {nm}", expanded=(i == 0)):
        c_a, c_b = st.columns([3, 1])
        s_nm = c_a.text_input("Subject", nm, key=f"n{i}")
        s_cr = c_b.number_input("Credits", 1, 6, cr, key=f"c{i}")
        c_c, c_d = st.columns(2)
        s_at = c_c.slider("Attendance (%)", 40, 100, at, key=f"a{i}")
        s_ls = c_d.number_input("Last Sem Exam (/100)", 0, 100, ls, key=f"l{i}")
        k1, k2, k3, k4 = st.columns(4)
        v1 = k1.number_input("Int 1 (/50)", 0, 50, i1, key=f"i1{i}")
        v2 = k2.number_input("Int 2 (/50)", 0, 50, i2, key=f"i2{i}")
        v3 = k3.number_input("Asg 1 (/5)", 0, 5, a1, key=f"a1{i}")
        v4 = k4.number_input("Asg 2 (/5)", 0, 5, a2, key=f"a2{i}")
        cie_val = round(((v1 + v2) / 100.0) * 40.0 + v3 + v4, 1)
        st.caption(f"Calculated CIE: {cie_val} / 50")
        rows.append({"Subject": s_nm, "Credits": s_cr, cols[0]: s_at, cols[1]: cie_val, cols[2]: s_ls})

if st.button("Predict SEE, Final Total (100), SGPA & CGPA"):
    sdf = pd.DataFrame(rows)
    sdf["Predicted SEE (/50)"] = model.predict(sdf[cols]).round(1)
    sdf["Final Total (/100)"] = (sdf[cols[1]] + sdf["Predicted SEE (/50)"]).round(1)
    res = [get_grade(t, c, s) for t, c, s in zip(sdf["Final Total (/100)"], sdf[cols[1]], sdf["Predicted SEE (/50)"])]
    sdf["GP"] = [r[0] for r in res]
    sdf["Grade"] = [r[1] for r in res]
    sgpa = (sdf["Credits"] * sdf["GP"]).sum() / sdf["Credits"].sum()
    ncgpa = ((curr_cgpa * comp_sems) + sgpa) / (comp_sems + 1)
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg Total", f"{sdf['Final Total (/100)'].mean():.1f} / 100")
    m2.metric("Semester SGPA", f"{sgpa:.2f} / 10")
    m3.metric("Projected CGPA", f"{ncgpa:.2f} / 10", f"{ncgpa - curr_cgpa:+.2f}")
    st.dataframe(sdf[["Subject", "Credits", cols[1], "Predicted SEE (/50)", "Final Total (/100)", "Grade", "GP"]], use_container_width=True)
    bad_cie = sdf[sdf[cols[1]] < 20]["Subject"].tolist()
    bad_att = sdf[sdf[cols[0]] < 75]["Subject"].tolist()
    if bad_cie: st.error(f"CIE Shortage (<20/50): {', '.join(bad_cie)}")
    if bad_att: st.warning(f"Attendance Shortage (<75%): {', '.join(bad_att)}")
    if not bad_cie and not bad_att: st.success("Eligible in all 6 subjects!")

st.divider()
st.subheader("Batch Class Analysis (Upload CSV)")
np.random.seed(99)
ns = 1000
fn = ["Aarav", "Diya", "Rohan", "Meera", "Kabir", "Ananya", "Vikram", "Priya", "Arjun", "Sneha"]
ln = ["Sharma", "Patel", "Reddy", "Nair", "Verma", "Gupta", "Iyer", "Singh", "Kumar", "Joshi"]
samp = pd.DataFrame({
    "Student Name": [f"{np.random.choice(fn)} {np.random.choice(ln)} (1RN23CS{100+i})" for i in range(ns)],
    "Attendance (%)": np.random.randint(52, 100, ns),
    "Internal 1 (/50)": np.random.randint(14, 50, ns),
    "Internal 2 (/50)": np.random.randint(15, 50, ns),
    "Assignment 1 (/5)": np.random.randint(2, 6, ns),
    "Assignment 2 (/5)": np.random.randint(2, 6, ns),
    "Last Sem Exam (/100)": np.random.randint(35, 98, ns),
    "Previous CGPA": np.round(np.random.uniform(5.4, 9.6, ns), 2)
})
st.download_button("Download 1,000-Student Dataset (CSV)", samp.to_csv(index=False).encode(), "rnsit_1000_students.csv", "text/csv")

up = st.file_uploader("Upload CSV", type=["csv"])
if up:
    bdf = pd.read_csv(up)
    if all(k in bdf.columns for k in ["Internal 1 (/50)", "Internal 2 (/50)", "Assignment 1 (/5)", "Assignment 2 (/5)"]):
        bdf[cols[1]] = (((bdf["Internal 1 (/50)"] + bdf["Internal 2 (/50)"]) / 100.0) * 40.0 + bdf["Assignment 1 (/5)"] + bdf["Assignment 2 (/5)"]).round(1)
    bdf["Predicted SEE (/50)"] = model.predict(bdf[cols]).round(1)
    bdf["Final Total (/100)"] = (bdf[cols[1]] + bdf["Predicted SEE (/50)"]).round(1)
    bres = [get_grade(t, c, s) for t, c, s in zip(bdf["Final Total (/100)"], bdf[cols[1]], bdf["Predicted SEE (/50)"])]
    bdf["SGPA"] = [r[0] for r in bres]
    bdf["Grade"] = [r[1] for r in bres]
    base_c = bdf["Previous CGPA"] if "Previous CGPA" in bdf.columns else (bdf[cols[2]] / 10.0)
    bdf["Projected CGPA"] = (((base_c * 3) + bdf["SGPA"]) / 4).round(2)
    bdf["Risk"] = np.where((bdf[cols[1]] < 20) | (bdf[cols[0]] < 75) | (bdf["Final Total (/100)"] < 45), "At Risk", "On Track")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Students", len(bdf))
    k2.metric("Avg Total", f"{bdf['Final Total (/100)'].mean():.1f}")
    k3.metric("Avg CGPA", f"{bdf['Projected CGPA'].mean():.2f}")
    k4.metric("At Risk", int((bdf["Risk"] == "At Risk").sum()))
    st.bar_chart(pd.cut(bdf["Final Total (/100)"], [0, 40, 60, 75, 100], labels=["Fail", "Second", "First", "FCD"]).value_counts())
    flt = st.radio("Filter:", ["All", "At-Risk Only"], horizontal=True)
    st.dataframe(bdf[bdf["Risk"] == "At Risk"] if flt == "At-Risk Only" else bdf, use_container_width=True)
    st.download_button("Download Report (CSV)", bdf.to_csv(index=False).encode(), "rnsit_report.csv", "text/csv")
    if "Student Name" in bdf.columns:
        sel = st.selectbox("Mentor Action Plan for:", bdf["Student Name"].head(100))
        sr = bdf[bdf["Student Name"] == sel].iloc[0]
        tgt = st.slider("Target Score (/100)", 45, 95, 75)
        st.text_area("Proctor Summary", f"Student: {sel}\nCIE: {sr[cols[1]]}/50 | SEE: {sr['Predicted SEE (/50)']}/50 | Total: {sr['Final Total (/100)']}/100\nSGPA: {sr['SGPA']} | Projected CGPA: {sr['Projected CGPA']} ({sr['Risk']})\nGoal Gap: +{max(0.0, tgt - sr['Final Total (/100)']):.1f} marks needed.", height=180)
