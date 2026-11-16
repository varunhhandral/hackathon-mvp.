import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("RNSIT / VTU Integrated Scheme: **CIE (50)** [Theory + Lab Internals] + **SEE (50)** [Theory + External Lab] = **Total (100)**, SGPA & CGPA.")

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
st.bar_chart(imp.set_index("Factor"))
st.divider()

st.subheader("6-Subject Semester Evaluation & CGPA (RNSIT Scheme)")
g1, g2 = st.columns(2)
curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, 7.65, 0.05)
comp_sems = g2.number_input("Completed Semesters", 1, 8, 3, 1)

# (Name, Credits, Att, Int1/50, Int2/50, Asg1/5, Asg2/5, ThisSem/100, HasLab, LabInt1/50, LabInt2/50, HasExtLab, ExtLab/50)
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
            l1, l2, l3 = st.columns([1, 1, 1])
            lv1 = l1.number_input("Lab Int 1 (/50)", 0, 50, li1, key=f"li1{i}")
            lv2 = l2.number_input("Lab Int 2 (/50)", 0, 50, li2, key=f"li2{i}")
            has_ext = l3.checkbox("External Lab Exam?", value=h_ext, key=f"he{i}")
            ext_val = st.number_input("External Lab Marks (/50)", 0, 50, ext_m if ext_m > 0 else 40, key=f"ex{i}") if has_ext else 0
            # Integrated CIE (50): Theory Int (25) + Assign (5) + Lab Int (20)
            cie_val = round(((v1 + v2) / 100.0) * 25.0 + ((v3 + v4) / 10.0) * 5.0 + ((lv1 + lv2) / 100.0) * 20.0, 1)
            # Integrated SEE (50): With Ext Lab -> Theory (35) + Ext Lab (15); Without -> Theory (50)
            see_val = round((s_ts / 100.0) * 35.0 + (ext_val / 50.0) * 15.0, 1) if has_ext else round(s_ts * 0.5, 1)
        else:
            # Theory-only CIE (50): Theory Int (40) + Assign (10); SEE (50): Theory (50)
            cie_val = round(((v1 + v2) / 100.0) * 40.0 + v3 + v4, 1)
            see_val = round(s_ts * 0.5, 1)

        tot_val = round(cie_val + see_val, 1)
        st.info(f"Scaled CIE: {cie_val}/50 | Scaled SEE: {see_val}/50 | Final Total: {tot_val}/100")
        rows.append({"Subject": s_nm, "Credits": s_cr, cols[0]: s_at, cols[1]: cie_val, cols[2]: s_ts, "SEE (/50)": see_val, "Final Total (/100)": tot_val})

if st.button("Calculate Final Marks, SGPA & CGPA"):
    sdf = pd.DataFrame(rows)
    res = [get_grade(t, c, s) for t, c, s in zip(sdf["Final Total (/100)"], sdf[cols[1]], sdf["SEE (/50)"])]
    sdf["GP"] = [r[0] for r in res]
    sdf["Grade"] = [r[1] for r in res]
    sgpa = (sdf["Credits"] * sdf["GP"]).sum() / sdf["Credits"].sum()
    ncgpa = ((curr_cgpa * comp_sems) + sgpa) / (comp_sems + 1)
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg Total", f"{sdf['Final Total (/100)'].mean():.1f} / 100")
    m2.metric("Semester SGPA", f"{sgpa:.2f} / 10")
    m3.metric("Projected CGPA", f"{ncgpa:.2f} / 10", f"{ncgpa - curr_cgpa:+.2f}")
    st.dataframe(sdf[["Subject", "Credits", cols[1], "SEE (/50)", "Final Total (/100)", "Grade", "GP"]], use_container_width=True)
    bad_cie = sdf[sdf[cols[1]] < 20]["Subject"].tolist()
    bad_att = sdf[sdf[cols[0]] < 75]["Subject"].tolist()
    if bad_cie: st.error(f"CIE Shortage (<20/50): {', '.join(bad_cie)}")
    if bad_att: st.warning(f"Attendance Shortage (<75%): {', '.join(bad_att)}")
    if not bad_cie and not bad_att: st.success("All 6 subjects cleared RNSIT CIE & Attendance rules!")

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
    "This Sem Exam (/100)": np.random.randint(35, 98, ns),
    "Previous CGPA": np.round(np.random.uniform(5.4, 9.6, ns), 2)
})
st.download_button("Download 1,000-Student Dataset (CSV)", samp.to_csv(index=False).encode(), "rnsit_1000_students.csv", "text/csv")

up = st.file_uploader("Upload CSV", type=["csv"])
if up:
    bdf = pd.read_csv(up)
    if all(k in bdf.columns for k in ["Internal 1 (/50)", "Internal 2 (/50)", "Assignment 1 (/5)", "Assignment 2 (/5)"]):
        bdf[cols[1]] = (((bdf["Internal 1 (/50)"] + bdf["Internal 2 (/50)"]) / 100.0) * 40.0 + bdf["Assignment 1 (/5)"] + bdf["Assignment 2 (/5)"]).round(1)
    bdf["SEE (/50)"] = (bdf[cols[2]] * 0.5).round(1)
    bdf["Final Total (/100)"] = (bdf[cols[1]] + bdf["SEE (/50)"]).round(1)
    bres = [get_grade(t, c, s) for t, c, s in zip(bdf["Final Total (/100)"], bdf[cols[1]], bdf["SEE (/50)"])]
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
        st.text_area("Proctor Summary", f"Student: {sel}\nCIE: {sr[cols[1]]}/50 | SEE: {sr['SEE (/50)']}/50 | Total: {sr['Final Total (/100)']}/100\nSGPA: {sr['SGPA']} | Projected CGPA: {sr['Projected CGPA']} ({sr['Risk']})\nGoal Gap: +{max(0.0, tgt - sr['Final Total (/100)']):.1f} marks needed.", height=180)
