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
</style>
<div class="hero">
  <h1>Student Performance & Placement Insights</h1>
  <p>Holistic RNSIT Analytics: Academics (CIE + SEE), Technical Skills & Final Year Placement Probability</p>
  <span class="pill">Academics + Skills</span>
  <span class="pill">Placement Probability (%)</span>
  <span class="pill">AI Study & Career Roadmap</span>
</div>
""", unsafe_allow_html=True)

# Train Academic SEE Model & Placement Probability Model
np.random.seed(42)
n_tr = 400
tr_att = np.random.randint(50, 100, n_tr)
tr_cie = np.random.uniform(15, 50, n_tr)
tr_see = np.clip(0.68 * tr_cie + 0.14 * tr_att + np.random.normal(0, 2.0, n_tr), 10, 50)
see_model = RandomForestRegressor(n_estimators=80, random_state=42).fit(np.column_stack([tr_att, tr_cie]), tr_see)

p_cgpa = np.random.uniform(5.2, 9.8, n_tr)
p_dsa = np.random.randint(25, 100, n_tr)
p_proj = np.random.randint(0, 6, n_tr)
p_intern = np.random.randint(0, 4, n_tr)
p_apt = np.random.randint(35, 100, n_tr)
p_prob = np.clip(p_cgpa * 4.2 + p_dsa * 0.28 + p_proj * 3.5 + p_intern * 7.5 + p_apt * 0.16 - 14 + np.random.normal(0, 2.5, n_tr), 8, 99.5)
place_model = RandomForestRegressor(n_estimators=80, random_state=42).fit(np.column_stack([p_cgpa, p_dsa, p_proj, p_intern, p_apt]), p_prob)

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
    g_map = {"O":"#dcfce7;color:#166534","A+":"#d1fae5;color:#065f46","A":"#dbeafe;color:#1e40af","B+":"#e0e7ff;color:#3730a3","B":"#fef3c7;color:#92400e","C":"#ffedd5;color:#9a3412","P":"#f3f4f6;color:#374151","F":"#fee2e2;color:#991b1b","Placement Ready":"#dcfce7;color:#166534","Needs Upskilling":"#fee2e2;color:#991b1b"}
    return f"background-color:{g_map[val]};font-weight:bold" if val in g_map else ""

def render_personal_dashboard(stu=None):
    if stu:
        if st.button("← Back to All Student Profiles"):
            st.session_state["active_stu"] = None
            st.rerun()
        st.markdown(f"""
        <div class="profile-banner">
          <strong style="color:#312e81;font-size:1.15rem;">360° Student Dashboard: {stu['Student Name']}</strong><br>
          <span style="color:#6d28d9;font-weight:600;font-size:0.86rem;">USN: {stu['USN']} &nbsp;|&nbsp; Placement Prob: {stu['Placement Prob (%)']}% &nbsp;|&nbsp; Academics + Technical Skills</span>
        </div>
        """, unsafe_allow_html=True)

    tab_acad, tab_place = st.tabs(["Academics & Study Planner", "Skills & Final Year Placement Predictor"])

    with tab_acad:
        g1, g2, g3 = st.columns([1, 1, 1.3])
        curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, float(stu["Previous CGPA"]) if stu and "Previous CGPA" in stu else 7.65, 0.05)
        comp_sems = g2.number_input("Completed Semesters", 1, 8, 5, 1)
        eval_mode = g3.radio("Internals Completed:", ["Both Internals (1 & 2)", "Only 1st Internal"])
        only_one = (eval_mode == "Only 1st Internal")

        d_att = int(stu["Attendance (%)"]) if stu else 84
        d_i1 = int(stu["Internal 1 (/50)"]) if stu and "Internal 1 (/50)" in stu else 41
        d_i2 = int(stu["Internal 2 (/50)"]) if stu and "Internal 2 (/50)" in stu else 39
        d_a1 = int(stu["Assignment 1 (/5)"]) if stu and "Assignment 1 (/5)" in stu else 5
        d_a2 = int(stu["Assignment 2 (/5)"]) if stu and "Assignment 2 (/5)" in stu else 4

        subs_init = [
            ("Data Structures", 4, d_att, d_i1, d_i2, d_a1, d_a2, True, 44, 46, True, 42),
            ("Operating Systems", 4, max(60, d_att-7), max(14, d_i1-11), max(15, d_i2-10), d_a1, d_a2, True, 36, 38, False, 0),
            ("Database Systems", 4, min(100, d_att+4), min(50, d_i1+4), min(50, d_i2+4), 5, 5, True, 45, 48, True, 44),
            ("Computer Networks", 3, max(58, d_att-9), max(12, d_i1-14), max(14, d_i2-13), 3, 3, False, 0, 0, False, 0),
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
                    k1, k2 = st.columns(2)
                    v1 = k1.number_input("Theory Int 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
                    v2 = v1
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
                    has_ext = l3.checkbox("External Lab?", value=h_ext, key=f"he_{uid}_{i}")
                    ext_val = st.number_input("External Lab (/50)", 0, 50, ext_m if ext_m > 0 else 40, key=f"ex_{uid}_{i}") if has_ext else 0
                    cie_val = round(((v1 + v2) / 100.0) * 25.0 + ((v3 + v4) / 10.0) * 5.0 + ((lv1 + lv2) / 100.0) * 20.0, 1)
                    raw_see = float(see_model.predict([[s_at, cie_val]])[0])
                    see_val = round((raw_see / 50.0) * 35.0 + (ext_val / 50.0) * 15.0, 1) if has_ext else round(raw_see, 1)
                else:
                    cie_val = round(((v1 + v2) / 100.0) * 40.0 + v3 + v4, 1)
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
            ncgpa = ((curr_cgpa * comp_sems) + sgpa) / (comp_sems + 1)
            st.session_state["proj_cgpa"] = round(ncgpa, 2)
            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Avg", f"{sdf['Predicted Total (/100)'].mean():.1f} / 100")
            m2.metric("Predicted SGPA", f"{sgpa:.2f} / 10")
            m3.metric("Projected CGPA", f"{ncgpa:.2f} / 10", f"{ncgpa - curr_cgpa:+.2f}")
            st.dataframe(sdf[["Subject", "Credits", "CIE (/50)", "Predicted SEE (/50)", "Predicted Total (/100)", "Grade", "GP"]].style.map(style_grade, subset=["Grade"]), use_container_width=True)
            strengths = sdf[sdf["Predicted Total (/100)"] >= 75]["Subject"].tolist()
            weaknesses = sdf[(sdf["Predicted Total (/100)"] < 60) | (sdf["CIE (/50)"] < 22)]["Subject"].tolist()
            c_sw1, c_sw2 = st.columns(2)
            c_sw1.markdown(f'<div class="sw-box sw-str"><strong>Academic Strengths (&ge;75)</strong><br>{", ".join(strengths) if strengths else "Keep pushing above 75"}</div>', unsafe_allow_html=True)
            c_sw2.markdown(f'<div class="sw-box sw-wk"><strong>Academic Weaknesses (&lt;60)</strong><br>{", ".join(weaknesses) if weaknesses else "No critical subject risk"}</div>', unsafe_allow_html=True)
            plan = [{"Subject": r["Subject"], "Weekly Hours": "8 hrs/wk" if r["Predicted Total (/100)"] < 60 else ("5 hrs/wk" if r["Predicted Total (/100)"] < 75 else "3 hrs/wk"), "Focus": "VTU Past Papers + CIE Recovery" if r["Predicted Total (/100)"] < 60 else "Module Revision + Mock Tests"} for _, r in sdf.iterrows()]
            st.dataframe(pd.DataFrame(plan), use_container_width=True)

    with tab_place:
        st.subheader("Technical Skills & Final Year Placement Readiness")
        uid_p = stu["USN"] if stu else "def_p"
        default_cgpa = st.session_state.get("proj_cgpa", float(stu["Projected CGPA"]) if stu and "Projected CGPA" in stu else 7.75)
        default_dsa = int(stu["DSA Score (/100)"]) if stu and "DSA Score (/100)" in stu else 68
        default_proj = int(stu["Projects"]) if stu and "Projects" in stu else 2
        default_int = int(stu["Internships"]) if stu and "Internships" in stu else 1
        default_apt = int(stu["Aptitude (/100)"]) if stu and "Aptitude (/100)" in stu else 72

        p1, p2 = st.columns(2)
        pl_cgpa = p1.number_input("Final Year CGPA (/10)", 0.0, 10.0, float(default_cgpa), 0.05, key=f"pcg_{uid_p}")
        pl_dsa = p2.slider("DSA & Coding Proficiency (/100)", 0, 100, default_dsa, key=f"pdsa_{uid_p}")

        p3, p4, p5 = st.columns(3)
        pl_proj = p3.number_input("Real-World Projects", 0, 10, default_proj, key=f"ppr_{uid_p}")
        pl_intern = p4.number_input("Internships Completed", 0, 5, default_int, key=f"pin_{uid_p}")
        pl_apt = p5.slider("Aptitude & Comm. (/100)", 0, 100, default_apt, key=f"pap_{uid_p}")

        all_skills = ["Python / Java / C++", "Data Structures & Algorithms", "Full-Stack Web (React/Node)", "SQL & DBMS", "Machine Learning / AI", "Cloud / Docker / Git", "System Design / OS"]
        init_sk = str(stu["Core Skills"]).split(", ") if stu and "Core Skills" in stu else ["Python / Java / C++", "SQL & DBMS", "Full-Stack Web (React/Node)"]
        init_sk = [s for s in init_sk if s in all_skills]
        sel_skills = st.multiselect("Verified Technical Skills:", all_skills, default=init_sk, key=f"psk_{uid_p}")

        raw_prob = float(place_model.predict([[pl_cgpa, pl_dsa, pl_proj, pl_intern, pl_apt]])[0])
        skill_bonus = len(sel_skills) * 1.4
        final_prob = round(min(99.2, max(10.0, raw_prob + skill_bonus - 4.0)), 1)

        if pl_cgpa >= 8.0 and pl_dsa >= 75 and len(sel_skills) >= 4 and final_prob >= 80:
            tier = "Tier-1 Product / Dream (10-24 LPA)"
        elif pl_cgpa >= 7.0 and final_prob >= 65:
            tier = "Tier-2 Tech / FinTech (6-10 LPA)"
        elif pl_cgpa >= 6.0 and final_prob >= 45:
            tier = "IT Services & Consulting (4-6 LPA)"
        else:
            tier = "Needs Pre-Placement Bootcamps"

        m1, m2, m3 = st.columns(3)
        m1.metric("Placement Probability", f"{final_prob}%")
        m2.metric("Skill Stack Score", f"{len(sel_skills)} / {len(all_skills)}")
        m3.metric("Target Package Tier", tier.split("(")[0].strip())

        st.markdown(f'<div class="score-badge">Predicted Final Year Placement Outcome: {final_prob}% Probability &nbsp;|&nbsp; Best Fit: {tier}</div>', unsafe_allow_html=True)

        missing_skills = [s for s in all_skills if s not in sel_skills]
        s_col1, s_col2 = st.columns(2)
        s_col1.markdown(f'<div class="sw-box sw-str"><strong>Placement Strengths</strong><br>Skills: {", ".join(sel_skills) if sel_skills else "None selected"}<br>CGPA Cutoff: {"Cleared (>=7.0)" if pl_cgpa >= 7.0 else "Below 7.0 (Restricts Dream Companies)"}</div>', unsafe_allow_html=True)
        s_col2.markdown(f'<div class="sw-box sw-wk"><strong>Skill Gaps to Close Before Placements</strong><br>Learn: {", ".join(missing_skills[:3]) if missing_skills else "All core skills covered!"}<br>Target: {"Solve 150+ LeetCode problems" if pl_dsa < 75 else "System Design & Mock Interviews"}</div>', unsafe_allow_html=True)

        roadmap = [
            {"Milestone": "Month 1: Coding & DSA", "Action Item": f"Raise DSA score from {pl_dsa}/100 to 80+ (Arrays, Trees, DP, Graphs)"},
            {"Milestone": "Month 2: Skill & Project Build", "Action Item": f"Build 1 end-to-end project using {missing_skills[0] if missing_skills else 'Cloud & System Design'}"},
            {"Milestone": "Month 3: Internship & Aptitude", "Action Item": f"{'Secure 1 summer internship + ' if pl_intern == 0 else ''}Practice quantitative aptitude & HR mock interviews"}
        ]
        st.dataframe(pd.DataFrame(roadmap), use_container_width=True)

# Main Router: Personal Dashboard vs 1,000-Student Profiles
if st.session_state.get("active_stu") is not None:
    render_personal_dashboard(st.session_state["active_stu"])
else:
    st.subheader("Batch Class Analysis (Upload CSV)")
    np.random.seed(99)
    ns = 1000
    fn = ["Nandini", "Kavya", "Abhishek", "Aarav", "Diya", "Rohan", "Meera", "Kabir", "Ananya", "Vikram"]
    ln = ["Nair", "Gowda", "Das", "Sharma", "Patel", "Reddy", "Verma", "Gupta", "Iyer", "Singh"]
    skill_pools = [
        "Python / Java / C++, Data Structures & Algorithms, SQL & DBMS, Full-Stack Web (React/Node)",
        "Python / Java / C++, Machine Learning / AI, SQL & DBMS",
        "Python / Java / C++, Full-Stack Web (React/Node), Cloud / Docker / Git, SQL & DBMS",
        "Python / Java / C++, SQL & DBMS"
    ]
    samp = pd.DataFrame({
        "Student Name": [f"{np.random.choice(fn)} {np.random.choice(ln)}" for _ in range(ns)],
        "USN": [f"1RN23CS{100+i}" for i in range(ns)],
        "Attendance (%)": np.random.randint(62, 100, ns),
        "Internal 1 (/50)": np.random.randint(18, 50, ns),
        "Internal 2 (/50)": np.random.randint(20, 50, ns),
        "Assignment 1 (/5)": np.random.randint(3, 6, ns),
        "Assignment 2 (/5)": np.random.randint(3, 6, ns),
        "Previous CGPA": np.round(np.random.uniform(6.0, 9.6, ns), 2),
        "DSA Score (/100)": np.random.randint(35, 98, ns),
        "Projects": np.random.randint(1, 5, ns),
        "Internships": np.random.randint(0, 3, ns),
        "Aptitude (/100)": np.random.randint(45, 96, ns),
        "Core Skills": [np.random.choice(skill_pools) for _ in range(ns)]
    })
    st.download_button("Download 1,000-Student Academic & Skills Dataset (CSV)", samp.to_csv(index=False).encode(), "rnsit_1000_students_placement.csv", "text/csv")

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
        base_c = bdf["Previous CGPA"] if "Previous CGPA" in bdf.columns else 7.5
        bdf["Projected CGPA"] = (((base_c * 3) + bdf["SGPA"]) / 4).round(2)

        if "DSA Score (/100)" not in bdf.columns: bdf["DSA Score (/100)"] = np.random.randint(45, 90, len(bdf))
        if "Projects" not in bdf.columns: bdf["Projects"] = np.random.randint(1, 4, len(bdf))
        if "Internships" not in bdf.columns: bdf["Internships"] = np.random.randint(0, 3, len(bdf))
        if "Aptitude (/100)" not in bdf.columns: bdf["Aptitude (/100)"] = np.random.randint(50, 92, len(bdf))
        if "Core Skills" not in bdf.columns: bdf["Core Skills"] = "Python / Java / C++, SQL & DBMS"

        raw_p = place_model.predict(bdf[["Projected CGPA", "DSA Score (/100)", "Projects", "Internships", "Aptitude (/100)"]].values)
        bdf["Placement Prob (%)"] = np.clip(raw_p, 12.0, 99.0).round(1)
        bdf["Status"] = np.where((bdf["Placement Prob (%)"] >= 65) & (bdf["Projected CGPA"] >= 6.5), "Placement Ready", "Needs Upskilling")

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Students", len(bdf))
        k2.metric("Avg CGPA", f"{bdf['Projected CGPA'].mean():.2f}")
        k3.metric("Avg Placement Prob", f"{bdf['Placement Prob (%)'].mean():.1f}%")
        k4.metric("Placement Ready", int((bdf["Status"] == "Placement Ready").sum()))

        st.subheader("Individual Student Profiles (Academics + Skills)")
        q = st.text_input("Search student name or ID", placeholder="e.g., Kavya or 1RN23CS105")
        filtered = bdf[bdf["Student Name"].str.contains(q, case=False, na=False) | bdf["USN"].str.contains(q, case=False, na=False)] if q else bdf

        grid_cols = st.columns(3)
        for idx, (_, r) in enumerate(filtered.head(9).iterrows()):
            initials = "".join([w[0] for w in str(r["Student Name"]).split()[:2]]).upper()
            tag_cls = "tag-ok" if r["Status"] == "Placement Ready" else "tag-risk"
            with grid_cols[idx % 3]:
                st.markdown(f"""
                <div class="stu-card">
                  <div class="stu-avatar">{initials}</div>
                  <p class="stu-name">{r['Student Name']}</p>
                  <p class="stu-id">ID: {r['USN']} | CGPA: {r['Projected CGPA']}</p>
                  <p class="stu-stat">DSA: {r['DSA Score (/100)']}/100 | Internships: {r['Internships']}</p>
                  <p class="stu-stat">Placement Prob: {r['Placement Prob (%)']}%</p>
                  <span class="{tag_cls}">{r['Status']}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Open Personal Dashboard", key=f"open_{r['USN']}_{idx}"):
                    st.session_state["active_stu"] = r.to_dict()
                    st.rerun()
    else:
        st.divider()
        render_personal_dashboard(None)
