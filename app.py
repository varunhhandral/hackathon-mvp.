import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Student Performance Insights", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Plus Jakarta Sans', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #eef2ff 0%, #fdf2f8 45%, #f0fdf4 100%);}
.hero {background: linear-gradient(125deg, #312e81 0%, #6d28d9 45%, #db2777 100%); padding: 24px; border-radius: 20px; color: white; margin-bottom: 18px; box-shadow: 0 12px 28px rgba(109,40,217,0.22);}
.hero h1 {margin: 0; font-size: 1.95rem; font-weight: 800; color: white;}
.hero p {margin: 6px 0 0; opacity: 0.92; font-size: 0.92rem;}
.pill {display: inline-block; background: rgba(255,255,255,0.18); padding: 4px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 600; margin: 8px 6px 0 0;}
div[data-testid="stMetric"] {background: rgba(255,255,255,0.92); border: 1px solid #e0e7ff; border-top: 4px solid #7c3aed; padding: 12px; border-radius: 14px; box-shadow: 0 4px 14px rgba(15,23,42,0.05);}
div[data-testid="stExpander"] {background: rgba(255,255,255,0.94); border-radius: 15px; border: 1.5px solid #ddd6fe; margin-bottom: 8px;}
div[data-testid="stExpander"] summary {background: linear-gradient(90deg, #f5f3ff, #fdf2f8); padding: 10px 14px; font-weight: 700; color: #312e81;}
div[data-baseweb="input"], div[data-baseweb="base-input"] {background: linear-gradient(135deg, #f5f3ff, #fdf4ff) !important; border: 1.5px solid #c4b5fd !important; border-radius: 10px !important;}
div[data-baseweb="input"] input {color: #1e1b4b !important; font-weight: 600 !important;}
button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {background-color: #ede9fe !important; color: #5b21b6 !important; border-radius: 8px !important;}
div[data-testid="stFileUploaderDropzone"] {background: linear-gradient(135deg, #eef2ff, #fce7f3) !important; border: 2px dashed #a855f7 !important; border-radius: 16px !important;}
div.stButton > button {background: linear-gradient(90deg, #4f46e5, #9333ea, #db2777); color: white; border: none; border-radius: 12px; font-weight: 700; width: 100%;}
div.stDownloadButton > button {background: linear-gradient(90deg, #0d9488, #0284c7); color: white; border: none; border-radius: 999px; font-weight: 600;}
.stu-card {background: rgba(255,255,255,0.96); border: 1.5px solid #e0e7ff; border-radius: 18px; padding: 18px 14px; text-align: center; box-shadow: 0 8px 20px rgba(99,102,241,0.08); margin-bottom: 8px;}
.stu-avatar {width: 54px; height: 54px; margin: 0 auto 10px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #ec4899); color: white; font-weight: 800; font-size: 1.15rem; display: flex; align-items: center; justify-content: center;}
.stu-name {font-size: 1.05rem; font-weight: 800; color: #1e1b4b; margin: 0;}
.stu-id {font-size: 0.8rem; color: #64748b; margin: 3px 0 10px; font-weight: 600;}
.stu-stat {font-size: 0.86rem; color: #334155; margin: 4px 0; font-weight: 600;}
.tag-ok {display: inline-block; background: #dcfce7; color: #166534; padding: 3px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; margin-top: 6px;}
.tag-risk {display: inline-block; background: #fee2e2; color: #991b1b; padding: 3px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; margin-top: 6px;}
.score-badge {background: linear-gradient(90deg, #eef2ff, #fae8ff); border-left: 4px solid #8b5cf6; padding: 9px 12px; border-radius: 10px; font-weight: 700; color: #1e1b4b; font-size: 0.88rem; margin-top: 6px;}
.profile-banner {background: linear-gradient(90deg, #eef2ff, #fdf2f8); border: 1.5px solid #c4b5fd; padding: 14px 18px; border-radius: 16px; margin-bottom: 14px;}
.sw-box {padding: 14px; border-radius: 14px; margin-bottom: 10px;}
.sw-str {background: #f0fdf4; border-left: 5px solid #16a34a; color: #14532d;}
.sw-wk {background: #fef2f2; border-left: 5px solid #dc2626; color: #7f1d1d;}
</style>
<div class="hero">
  <h1>Student Performance Insights</h1>
  <p>AI-Powered RNSIT Final Marks Predictor (From 1 or 2 Internals), Strength/Weakness Analyzer & Study Planner</p>
  <span class="pill">1-Internal or 2-Internal Prediction</span>
  <span class="pill">CIE (50) + Predicted SEE (50)</span>
  <span class="pill">AI Study Planner</span>
</div>
""", unsafe_allow_html=True)

# Train SEE Predictor Model (Attendance + CIE -> Predicted SEE out of 50)
np.random.seed(42)
n_tr = 400
tr_att = np.random.randint(50, 100, n_tr)
tr_cie = np.random.uniform(15, 50, n_tr)
tr_see = np.clip(0.68 * tr_cie + 0.14 * tr_att + np.random.normal(0, 2.0, n_tr), 10, 50)
see_model = RandomForestRegressor(n_estimators=100, random_state=42).fit(np.column_stack([tr_att, tr_cie]), tr_see)

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
    g_map = {"O":"#dcfce7;color:#166534","A+":"#d1fae5;color:#065f46","A":"#dbeafe;color:#1e40af","B+":"#e0e7ff;color:#3730a3","B":"#fef3c7;color:#92400e","C":"#ffedd5;color:#9a3412","P":"#f3f4f6;color:#374151","F":"#fee2e2;color:#991b1b","At Risk":"#fee2e2;color:#991b1b","On Track":"#dcfce7;color:#166534"}
    return f"background-color:{g_map[val]};font-weight:bold" if val in g_map else ""

def render_personal_dashboard(stu=None):
    if stu:
        if st.button("← Back to All Student Profiles"):
            st.session_state["active_stu"] = None
            st.rerun()
        st.markdown(f"""
        <div class="profile-banner">
          <strong style="color:#312e81;font-size:1.15rem;">Personal AI Dashboard: {stu['Student Name']}</strong><br>
          <span style="color:#6d28d9;font-weight:600;font-size:0.88rem;">USN: {stu['USN']} &nbsp;|&nbsp; Status: {stu['Risk']} &nbsp;|&nbsp; Predict Final Marks from 1 or 2 Internals</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.subheader("Personal AI Dashboard: 6-Subject Predictor & Study Planner")

    g1, g2, g3 = st.columns([1, 1, 1.3])
    curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, float(stu["Previous CGPA"]) if stu and "Previous CGPA" in stu else 7.45, 0.05)
    comp_sems = g2.number_input("Completed Semesters", 1, 8, 3, 1)
    eval_mode = g3.radio("Internals Completed:", ["Both Internals (1 & 2)", "Only 1st Internal"], horizontal=False)
    only_one = (eval_mode == "Only 1st Internal")

    d_att = int(stu["Attendance (%)"]) if stu else 84
    d_i1 = int(stu["Internal 1 (/50)"]) if stu and "Internal 1 (/50)" in stu else 41
    d_i2 = int(stu["Internal 2 (/50)"]) if stu and "Internal 2 (/50)" in stu else 39
    d_a1 = int(stu["Assignment 1 (/5)"]) if stu and "Assignment 1 (/5)" in stu else 5
    d_a2 = int(stu["Assignment 2 (/5)"]) if stu and "Assignment 2 (/5)" in stu else 4

    subs_init = [
        ("Data Structures", 4, d_att, d_i1, d_i2, d_a1, d_a2, True, 44, 46, True, 42),
        ("Operating Systems", 4, max(60, d_att-7), max(14, d_i1-12), max(15, d_i2-11), d_a1, d_a2, True, 36, 38, False, 0),
        ("Database Systems", 4, min(100, d_att+4), min(50, d_i1+4), min(50, d_i2+4), 5, 5, True, 45, 48, True, 44),
        ("Computer Networks", 3, max(58, d_att-10), max(12, d_i1-15), max(14, d_i2-14), 3, 3, False, 0, 0, False, 0),
        ("Discrete Maths", 4, d_att, max(18, d_i1-4), max(18, d_i2-3), 4, 5, False, 0, 0, False, 0),
        ("Software Engg", 3, min(100, d_att+5), min(50, d_i1+5), min(50, d_i2+5), 5, 5, False, 0, 0, False, 0)
    ]

    uid = stu["USN"] if stu else "default"
    rows = []
    for i, (nm, cr, at, i1, i2, a1, a2, h_lab, li1, li2, h_ext, ext_m) in enumerate(subs_init):
        with st.expander(f"Subject {i+1}: {nm}", expanded=(i == 0)):
            c_a, c_b, c_c = st.columns([2.4, 0.9, 1.7])
            s_nm = c_a.text_input("Subject Name", nm, key=f"n_{uid}_{i}")
            s_cr = c_b.number_input("Credits", 1, 6, cr, key=f"c_{uid}_{i}")
            s_at = c_c.slider("Attendance (%)", 40, 100, at, key=f"a_{uid}_{i}")

            if only_one:
                k1, k2, k3 = st.columns(3)
                v1 = k1.number_input("Theory Int 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
                v2 = v1  # Project Int 2 from Int 1
                v3 = k2.number_input("Assign 1 (/5)", 0, 5, a1, key=f"a1_{uid}_{i}")
                v4 = v3
            else:
                k1, k2, k3, k4 = st.columns(4)
                v1 = k1.number_input("Theory Int 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
                v2 = k2.number_input("Theory Int 2 (/50)", 0, 50, i2, key=f"i2_{uid}_{i}")
                v3 = k3.number_input("Assign 1 (/5)", 0, 5, a1, key=f"a1_{uid}_{i}")
                v4 = k4.number_input("Assign 2 (/5)", 0, 5, a2, key=f"a2_{uid}_{i}")

            has_lab = st.checkbox("Include Lab Component?", value=h_lab, key=f"hl_{uid}_{i}")
            if has_lab:
                l1, l2, l3 = st.columns(3)
                lv1 = l1.number_input("Lab Int 1 (/50)", 0, 50, li1, key=f"li1_{uid}_{i}")
                lv2 = lv1 if only_one else l2.number_input("Lab Int 2 (/50)", 0, 50, li2, key=f"li2_{uid}_{i}")
                has_ext = l3.checkbox("External Lab Exam?", value=h_ext, key=f"he_{uid}_{i}")
                ext_val = st.number_input("External Lab (/50)", 0, 50, ext_m if ext_m > 0 else 40, key=f"ex_{uid}_{i}") if has_ext else 0
                cie_val = round(((v1 + v2) / 100.0) * 25.0 + ((v3 + v4) / 10.0) * 5.0 + ((lv1 + lv2) / 100.0) * 20.0, 1)
                raw_see = float(see_model.predict([[s_at, cie_val]])[0])
                see_val = round((raw_see / 50.0) * 35.0 + (ext_val / 50.0) * 15.0, 1) if has_ext else round(raw_see, 1)
            else:
                cie_val = round(((v1 + v2) / 100.0) * 40.0 + v3 + v4, 1)
                see_val = round(float(see_model.predict([[s_at, cie_val]])[0]), 1)

            tot_val = round(min(100.0, cie_val + see_val), 1)
            mode_lbl = "1-Int Projection" if only_one else "2-Int Evaluation"
            st.markdown(f'<div class="score-badge">{mode_lbl} &rarr; CIE: {cie_val}/50 &nbsp;|&nbsp; Predicted SEE: {see_val}/50 &nbsp;|&nbsp; Predicted Final: {tot_val}/100</div>', unsafe_allow_html=True)
            rows.append({"Subject": s_nm, "Credits": s_cr, "Attendance (%)": s_at, "CIE (/50)": cie_val, "Predicted SEE (/50)": see_val, "Predicted Total (/100)": tot_val})

    if st.button("Predict Final Marks, SGPA & Generate Study Planner"):
        sdf = pd.DataFrame(rows)
        res = [get_grade(t, c, s) for t, c, s in zip(sdf["Predicted Total (/100)"], sdf["CIE (/50)"], sdf["Predicted SEE (/50)"])]
        sdf["GP"] = [r[0] for r in res]
        sdf["Grade"] = [r[1] for r in res]
        sgpa = (sdf["Credits"] * sdf["GP"]).sum() / sdf["Credits"].sum()
        ncgpa = ((curr_cgpa * comp_sems) + sgpa) / (comp_sems + 1)

        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Avg", f"{sdf['Predicted Total (/100)'].mean():.1f} / 100")
        m2.metric("Predicted SGPA", f"{sgpa:.2f} / 10")
        m3.metric("Projected CGPA", f"{ncgpa:.2f} / 10", f"{ncgpa - curr_cgpa:+.2f}")

        show_s = sdf[["Subject", "Credits", "CIE (/50)", "Predicted SEE (/50)", "Predicted Total (/100)", "Grade", "GP"]]
        st.dataframe(show_s.style.map(style_grade, subset=["Grade"]), use_container_width=True)

        # Strength & Weakness Analysis
        st.subheader("AI Strength & Weakness Diagnosis")
        strengths = sdf[sdf["Predicted Total (/100)"] >= 75]["Subject"].tolist()
        weaknesses = sdf[(sdf["Predicted Total (/100)"] < 60) | (sdf["CIE (/50)"] < 22)]["Subject"].tolist()
        moderate = sdf[(sdf["Predicted Total (/100)"] >= 60) & (sdf["Predicted Total (/100)"] < 75) & (sdf["CIE (/50)"] >= 22)]["Subject"].tolist()

        c_sw1, c_sw2 = st.columns(2)
        with c_sw1:
            str_txt = ", ".join(strengths) if strengths else "Focus on building 75+ mastery in top subjects"
            st.markdown(f'<div class="sw-box sw-str"><strong>Core Strengths (&ge;75 Marks)</strong><br>{str_txt}<br><small>Action: Aim for O/A+ grade (90+) to boost SGPA.</small></div>', unsafe_allow_html=True)
        with c_sw2:
            wk_txt = ", ".join(weaknesses) if weaknesses else "No critical weak subjects detected!"
            st.markdown(f'<div class="sw-box sw-wk"><strong>Priority Weaknesses (&lt;60 or Low CIE)</strong><br>{wk_txt}<br><small>Action: Immediate revision + CIE improvement test.</small></div>', unsafe_allow_html=True)

        # Personalized Weekly Study Planner
        st.subheader("Personalized 4-Week Study & Recovery Planner")
        plan_rows = []
        for _, r in sdf.iterrows():
            tot, cie_m, att_m = r["Predicted Total (/100)"], r["CIE (/50)"], r["Attendance (%)"]
            if cie_m < 20 or tot < 55:
                prio, hrs, focus = "High Priority (Weak)", "8 hrs/week", "Basics + Past 5-Yr VTU Papers + Improvement Test"
            elif tot < 75 or att_m < 75:
                prio, hrs, focus = "Medium (Moderate)", "5 hrs/week", "Module-wise Numericals + Lab Viva + Attendance >=80%"
            else:
                prio, hrs, focus = "Maintain (Strength)", "3 hrs/week", "Mock Tests + High-Weightage 10-Mark Questions"
            plan_rows.append({"Subject": r["Subject"], "Category": prio, "Weekly Target": hrs, "Recommended Study Focus": focus})
        st.dataframe(pd.DataFrame(plan_rows), use_container_width=True)

# Main Router: Personal Dashboard vs 1,000-Student Profiles
if st.session_state.get("active_stu") is not None:
    render_personal_dashboard(st.session_state["active_stu"])
else:
    st.subheader("Batch Class Analysis (Upload CSV)")
    np.random.seed(99)
    ns = 1000
    fn = ["Nandini", "Kavya", "Abhishek", "Aarav", "Diya", "Rohan", "Meera", "Kabir", "Ananya", "Vikram"]
    ln = ["Nair", "Gowda", "Das", "Sharma", "Patel", "Reddy", "Verma", "Gupta", "Iyer", "Singh"]
    samp = pd.DataFrame({
        "Student Name": [f"{np.random.choice(fn)} {np.random.choice(ln)}" for _ in range(ns)],
        "USN": [f"1RN23CS{100+i}" for i in range(ns)],
        "Attendance (%)": np.random.randint(58, 100, ns),
        "Internal 1 (/50)": np.random.randint(16, 50, ns),
        "Internal 2 (/50)": np.random.randint(18, 50, ns),
        "Assignment 1 (/5)": np.random.randint(2, 6, ns),
        "Assignment 2 (/5)": np.random.randint(2, 6, ns),
        "Previous CGPA": np.round(np.random.uniform(5.8, 9.6, ns), 2)
    })
    st.download_button("Download 1,000-Student Dataset (CSV)", samp.to_csv(index=False).encode(), "rnsit_1000_students.csv", "text/csv")

    up = st.file_uploader("Upload CSV", type=["csv"])
    if up is not None:
        st.session_state["batch_csv"] = pd.read_csv(up)

    if "batch_csv" in st.session_state:
        bdf = st.session_state["batch_csv"].copy()
        if "USN" not in bdf.columns:
            bdf["USN"] = [f"1RN23CS{100+i}" for i in range(len(bdf))]
        if all(k in bdf.columns for k in ["Internal 1 (/50)", "Internal 2 (/50)", "Assignment 1 (/5)", "Assignment 2 (/5)"]):
            bdf["CIE (/50)"] = (((bdf["Internal 1 (/50)"] + bdf["Internal 2 (/50)"]) / 100.0) * 40.0 + bdf["Assignment 1 (/5)"] + bdf["Assignment 2 (/5)"]).round(1)
        elif "CIE (/50)" not in bdf.columns:
            bdf["CIE (/50)"] = 35.0
        bdf["Predicted SEE (/50)"] = see_model.predict(bdf[["Attendance (%)", "CIE (/50)"]].values).round(1)
        bdf["Predicted Total (/100)"] = (bdf["CIE (/50)"] + bdf["Predicted SEE (/50)"]).round(1)
        bres = [get_grade(t, c, s) for t, c, s in zip(bdf["Predicted Total (/100)"], bdf["CIE (/50)"], bdf["Predicted SEE (/50)"])]
        bdf["SGPA"] = [r[0] for r in bres]
        bdf["Grade"] = [r[1] for r in bres]
        base_c = bdf["Previous CGPA"] if "Previous CGPA" in bdf.columns else 7.5
        bdf["Projected CGPA"] = (((base_c * 3) + bdf["SGPA"]) / 4).round(2)
        bdf["Pass Prob (%)"] = np.clip((bdf["Predicted Total (/100)"] * 1.45 + bdf["Attendance (%)"] * 0.25), 12.0, 100.0).round(2)
        bdf["Risk"] = np.where((bdf["CIE (/50)"] < 20) | (bdf["Attendance (%)"] < 75) | (bdf["Predicted Total (/100)"] < 45), "At Risk", "On Track")

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Students", len(bdf))
        k2.metric("Avg Predicted", f"{bdf['Predicted Total (/100)'].mean():.1f}")
        k3.metric("Avg CGPA", f"{bdf['Projected CGPA'].mean():.2f}")
        k4.metric("At Risk", int((bdf["Risk"] == "At Risk").sum()))

        st.subheader("Individual Student Profiles")
        q = st.text_input("Search student name or ID", placeholder="e.g., Nandini or 1RN23CS105")
        filtered = bdf[bdf["Student Name"].str.contains(q, case=False, na=False) | bdf["USN"].str.contains(q, case=False, na=False)] if q else bdf

        grid_cols = st.columns(3)
        for idx, (_, r) in enumerate(filtered.head(9).iterrows()):
            initials = "".join([w[0] for w in str(r["Student Name"]).split()[:2]]).upper()
            tag_cls = "tag-ok" if r["Risk"] == "On Track" else "tag-risk"
            with grid_cols[idx % 3]:
                st.markdown(f"""
                <div class="stu-card">
                  <div class="stu-avatar">{initials}</div>
                  <p class="stu-name">{r['Student Name']}</p>
                  <p class="stu-id">ID: {r['USN']}</p>
                  <p class="stu-stat">Predicted Marks: {r['Predicted Total (/100)']}</p>
                  <p class="stu-stat">Pass Probability: {r['Pass Prob (%)']}%</p>
                  <span class="{tag_cls}">{r['Risk']}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Open Personal Dashboard", key=f"open_{r['USN']}_{idx}"):
                    st.session_state["active_stu"] = r.to_dict()
                    st.rerun()
    else:
        st.divider()
        render_personal_dashboard(None)
