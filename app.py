import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Student Performance & Placement Insights", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Plus Jakarta Sans', sans-serif;}
.stApp {background: radial-gradient(circle at top left, #eef2ff 0%, #fdf2f8 45%, #f0fdf4 100%);}
.hero {background: linear-gradient(125deg, #312e81 0%, #6d28d9 45%, #db2777 100%); padding: 24px; border-radius: 20px; color: white; margin-bottom: 18px; box-shadow: 0 12px 28px rgba(109,40,217,0.22);}
.hero h1 {margin: 0; font-size: 1.9rem; font-weight: 800; color: white;}
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
.stu-card {background: rgba(255,255,255,0.96); border: 1.5px solid #e0e7ff; border-radius: 18px; padding: 16px 12px; text-align: center; box-shadow: 0 8px 20px rgba(99,102,241,0.08); margin-bottom: 8px;}
.stu-avatar {width: 50px; height: 50px; margin: 0 auto 8px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #ec4899); color: white; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;}
.stu-name {font-size: 1.02rem; font-weight: 800; color: #1e1b4b; margin: 0;}
.stu-id {font-size: 0.78rem; color: #64748b; margin: 2px 0 8px; font-weight: 600;}
.stu-stat {font-size: 0.83rem; color: #334155; margin: 3px 0; font-weight: 600;}
.tag-ok {display: inline-block; background: #dcfce7; color: #166534; padding: 3px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 700; margin-top: 6px;}
.tag-risk {display: inline-block; background: #fee2e2; color: #991b1b; padding: 3px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 700; margin-top: 6px;}
.score-badge {background: linear-gradient(90deg, #eef2ff, #fae8ff); border-left: 4px solid #8b5cf6; padding: 9px 12px; border-radius: 10px; font-weight: 700; color: #1e1b4b; font-size: 0.86rem; margin-top: 6px;}
.profile-banner {background: linear-gradient(90deg, #eef2ff, #fdf2f8); border: 1.5px solid #c4b5fd; padding: 14px 18px; border-radius: 16px; margin-bottom: 14px;}
.sw-box {padding: 13px; border-radius: 14px; margin-bottom: 10px;}
.sw-str {background: #f0fdf4; border-left: 5px solid #16a34a; color: #14532d;}
.sw-wk {background: #fef2f2; border-left: 5px solid #dc2626; color: #7f1d1d;}
.fac-card {background: rgba(255,255,255,0.95); border-left: 5px solid #6366f1; padding: 14px 16px; border-radius: 14px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);}
</style>
<div class="hero">
  <h1>Student Performance & Placement Insights</h1>
  <p>RNSIT Academic Predictor, Minimum CGPA Cutoff Tracker & Faculty Teaching Co-Pilot</p>
  <span class="pill">CIE (50) + Predicted SEE (50)</span>
  <span class="pill">Min CGPA Cutoff Tracker</span>
  <span class="pill">Faculty & Mentor Insights</span>
</div>
""", unsafe_allow_html=True)

np.random.seed(42)
n_tr = 400
tr_att = np.random.randint(50, 100, n_tr)
tr_cie = np.random.uniform(15, 50, n_tr)
tr_see = np.clip(0.68 * tr_cie + 0.14 * tr_att + np.random.normal(0, 2.0, n_tr), 10, 50)
see_model = RandomForestRegressor(n_estimators=80, random_state=42).fit(np.column_stack([tr_att, tr_cie]), tr_see)

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
    g_map = {"O":"#dcfce7;color:#166534","A+":"#d1fae5;color:#065f46","A":"#dbeafe;color:#1e40af","B+":"#e0e7ff;color:#3730a3","B":"#fef3c7;color:#92400e","C":"#ffedd5;color:#9a3412","P":"#f3f4f6;color:#374151","F":"#fee2e2;color:#991b1b","Eligible (Cutoff Cleared)":"#dcfce7;color:#166534","Below Min CGPA":"#fee2e2;color:#991b1b"}
    return f"background-color:{g_map[val]};font-weight:bold" if val in g_map else ""

def render_personal_dashboard(stu=None):
    if stu:
        if st.button("← Back to All Student Profiles"):
            st.session_state["active_stu"] = None
            st.rerun()
        st.markdown(f"""
        <div class="profile-banner">
          <strong style="color:#312e81;font-size:1.15rem;">360° Student Dashboard: {stu['Student Name']}</strong><br>
          <span style="color:#6d28d9;font-weight:600;font-size:0.86rem;">USN: {stu['USN']} &nbsp;|&nbsp; Status: {stu['Status']} &nbsp;|&nbsp; Academics & Min CGPA Placement Eligibility</span>
        </div>
        """, unsafe_allow_html=True)

    tab_acad, tab_place = st.tabs(["Academics & Study Planner", "Min CGPA Cutoff & Placement Skills"])

    with tab_acad:
        eval_mode = st.radio("Internals Completed:", ["Both Internals (1 & 2)", "Only 1st Internal"], horizontal=True)
        only_one = (eval_mode == "Only 1st Internal")

        d_att = int(stu["Attendance (%)"]) if stu else 84
        d_i1 = int(stu["Internal 1 (/50)"]) if stu and "Internal 1 (/50)" in stu else 41
        d_i2 = int(stu["Internal 2 (/50)"]) if stu and "Internal 2 (/50)" in stu else 39

        subs_init = [
            ("Data Structures", 4, d_att, d_i1, d_i2),
            ("Operating Systems", 4, max(60, d_att-7), max(14, d_i1-11), max(15, d_i2-10)),
            ("Database Systems", 4, min(100, d_att+4), min(50, d_i1+4), min(50, d_i2+4)),
            ("Computer Networks", 3, max(58, d_att-9), max(12, d_i1-14), max(14, d_i2-13)),
            ("Discrete Maths", 4, d_att, max(18, d_i1-4), max(18, d_i2-3)),
            ("Software Engg", 3, min(100, d_att+5), min(50, d_i1+5), min(50, d_i2+5))
        ]

        uid = stu["USN"] if stu else "default"
        rows = []
        for i, (nm, cr, at, i1, i2) in enumerate(subs_init):
            with st.expander(f"Subject {i+1}: {nm}", expanded=(i == 0)):
                c_a, c_b, c_c = st.columns([2.4, 0.9, 1.7])
                s_nm = c_a.text_input("Subject Name", nm, key=f"n_{uid}_{i}")
                s_cr = c_b.number_input("Credits", 1, 6, cr, key=f"c_{uid}_{i}")
                s_at = c_c.slider("Attendance (%)", 40, 100, at, key=f"a_{uid}_{i}")
                if only_one:
                    v1 = st.number_input("Internal 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
                    v2 = v1
                else:
                    k1, k2 = st.columns(2)
                    v1 = k1.number_input("Internal 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
                    v2 = k2.number_input("Internal 2 (/50)", 0, 50, i2, key=f"i2_{uid}_{i}")

                cie_val = round(((v1 + v2) / 100.0) * 50.0, 1)
                see_val = round(float(see_model.predict([[s_at, cie_val]])[0]), 1)
                tot_val = round(min(100.0, cie_val + see_val), 1)
                st.markdown(f'<div class="score-badge">CIE: {cie_val}/50 &nbsp;|&nbsp; Predicted SEE: {see_val}/50 &nbsp;|&nbsp; Predicted Final: {tot_val}/100</div>', unsafe_allow_html=True)
                rows.append({"Subject": s_nm, "Credits": s_cr, "Attendance (%)": s_at, "CIE (/50)": cie_val, "Predicted SEE (/50)": see_val, "Predicted Total (/100)": tot_val})

        if st.button("Predict Academics & Generate Study Planner", key=f"btn_ac_{uid}"):
            sdf = pd.DataFrame(rows)
            res = [get_grade(t, c, s) for t, c, s in zip(sdf["Predicted Total (/100)"], sdf["CIE (/50)"], sdf["Predicted SEE (/50)"])]
            sdf["GP"] = [r[0] for r in res]
            sdf["Grade"] = [r[1] for r in res]
            sgpa = (sdf["Credits"] * sdf["GP"]).sum() / sdf["Credits"].sum()
            st.session_state["calc_sgpa"] = round(sgpa, 2)
            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Avg", f"{sdf['Predicted Total (/100)'].mean():.1f} / 100")
            m2.metric("Predicted SGPA", f"{sgpa:.2f} / 10")
            m3.metric("Subjects Passed", f"{int((sdf['Grade'] != 'F').sum())} / 6")
            st.dataframe(sdf[["Subject", "Credits", "CIE (/50)", "Predicted SEE (/50)", "Predicted Total (/100)", "Grade", "GP"]].style.map(style_grade, subset=["Grade"]), use_container_width=True)
            strengths = sdf[sdf["Predicted Total (/100)"] >= 75]["Subject"].tolist()
            weaknesses = sdf[(sdf["Predicted Total (/100)"] < 60) | (sdf["CIE (/50)"] < 22)]["Subject"].tolist()
            c_sw1, c_sw2 = st.columns(2)
            c_sw1.markdown(f'<div class="sw-box sw-str"><strong>Academic Strengths (&ge;75)</strong><br>{", ".join(strengths) if strengths else "Keep pushing above 75"}</div>', unsafe_allow_html=True)
            c_sw2.markdown(f'<div class="sw-box sw-wk"><strong>Academic Weaknesses (&lt;60)</strong><br>{", ".join(weaknesses) if weaknesses else "No critical subject risk"}</div>', unsafe_allow_html=True)
            plan = [{"Subject": r["Subject"], "Weekly Hours": "8 hrs/wk" if r["Predicted Total (/100)"] < 60 else ("5 hrs/wk" if r["Predicted Total (/100)"] < 75 else "3 hrs/wk"), "Focus": "VTU Past Papers + CIE Recovery" if r["Predicted Total (/100)"] < 60 else "Module Revision + Mock Tests"} for _, r in sdf.iterrows()]
            st.dataframe(pd.DataFrame(plan), use_container_width=True)

    with tab_place:
        st.subheader("Minimum CGPA Placement Eligibility & Skills")
        uid_p = stu["USN"] if stu else "def_p"
        stu_sgpa = st.session_state.get("calc_sgpa", float(stu["SGPA"]) if stu and "SGPA" in stu else 7.50)

        p1, p2 = st.columns(2)
        min_cutoff = p1.number_input("Min Placement CGPA Cutoff", 5.0, 9.5, 7.0, 0.25, key=f"pcut_{uid_p}")
        sems_done = p2.number_input("Semesters Completed", 1, 7, 5, 1, key=f"psem_{uid_p}")

        rem_sems = max(1, 7 - sems_done)
        cgpa_diff = round(stu_sgpa - min_cutoff, 2)
        req_sgpa = round(((min_cutoff * (sems_done + rem_sems)) - (stu_sgpa * sems_done)) / rem_sems, 2)

        all_skills = ["Python / Java / C++", "Data Structures & Algorithms", "Full-Stack Web (React/Node)", "SQL & DBMS", "Machine Learning / AI", "Cloud / Docker / Git", "System Design / OS"]
        init_sk = str(stu["Core Skills"]).split(", ") if stu and "Core Skills" in stu else ["Python / Java / C++", "SQL & DBMS"]
        init_sk = [s for s in init_sk if s in all_skills]
        sel_skills = st.multiselect("Verified Skills (For Placement Drive):", all_skills, default=init_sk, key=f"psk_{uid_p}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score vs Min Cutoff", f"{stu_sgpa:.2f} / {min_cutoff:.2f}", f"{cgpa_diff:+.2f}")
        c2.metric("Cutoff Status", "CLEARED" if stu_sgpa >= min_cutoff else "NOT MET")
        c3.metric("Required SGPA Next Sem", "Maintained" if stu_sgpa >= min_cutoff else f"{min(10.0, max(0.0, req_sgpa)):.2f} / 10")

        if stu_sgpa >= min_cutoff:
            st.markdown(f'<div class="score-badge">Eligible for Campus Placements! Student has crossed the {min_cutoff:.2f} minimum CGPA cutoff (+{cgpa_diff:.2f} buffer).</div>', unsafe_allow_html=True)
        else:
            if req_sgpa <= 10.0:
                st.error(f"Below Minimum CGPA Cutoff by {abs(cgpa_diff):.2f} points. Student must score an average SGPA of {req_sgpa:.2f} across the remaining {rem_sems} semester(s) before final year placements to cross {min_cutoff:.2f} CGPA.")
            else:
                st.error(f"Below Minimum CGPA Cutoff ({stu_sgpa:.2f} < {min_cutoff:.2f}). Focus on skill-based off-campus drives & companies with 6.0–6.5 CGPA criteria.")

        missing_skills = [s for s in all_skills if s not in sel_skills]
        s_col1, s_col2 = st.columns(2)
