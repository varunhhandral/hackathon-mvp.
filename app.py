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
.stu-card {background: rgba(255,255,255,0.96); border: 1.5px solid #e0e7ff; border-radius: 18px; padding: 16px 12px; text-align: center; box-shadow: 0 8px 20px rgba(99,102,241,0.08); margin-bottom: 8px;}
.stu-avatar {width: 50px; height: 50px; margin: 0 auto 8px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #ec4899); color: white; font-weight: 800; font-size: 1.1rem; display: flex; align-items: center; justify-content: center;}
.stu-name {font-size: 1.02rem; font-weight: 800; color: #1e1b4b; margin: 0;}
.stu-id {font-size: 0.78rem; color: #64748b; margin: 2px 0 8px; font-weight: 600;}
.stu-stat {font-size: 0.83rem; color: #334155; margin: 3px 0; font-weight: 600;}
.tag-ok {display: inline-block; background: #dcfce7; color: #166534; padding: 3px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 700; margin-top: 6px;}
.tag-warn {display: inline-block; background: #fef3c7; color: #92400e; padding: 3px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 700; margin-top: 6px;}
.tag-risk {display: inline-block; background: #fee2e2; color: #991b1b; padding: 3px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 700; margin-top: 6px;}
.score-badge {background: linear-gradient(90deg, #eef2ff, #fae8ff); border-left: 4px solid #8b5cf6; padding: 10px 14px; border-radius: 10px; font-weight: 700; color: #1e1b4b; font-size: 0.88rem; margin-top: 6px;}
.profile-banner {background: linear-gradient(90deg, #eef2ff, #fdf2f8); border: 1.5px solid #c4b5fd; padding: 14px 18px; border-radius: 16px; margin-bottom: 14px;}
.sw-box {padding: 13px; border-radius: 14px; margin-bottom: 10px;}
.sw-str {background: #f0fdf4; border-left: 5px solid #16a34a; color: #14532d;}
.sw-wk {background: #fef2f2; border-left: 5px solid #dc2626; color: #7f1d1d;}
.fac-card {background: rgba(255,255,255,0.95); border-left: 5px solid #6366f1; padding: 14px 16px; border-radius: 14px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.04);}
</style>
<div class="hero">
  <h1>Student Performance & Placement Insights</h1>
  <p>RNSIT Academic Predictor, Step-by-Step Score & Skill Upgrader & Faculty Teaching Co-Pilot</p>
  <span class="pill">CIE (50) + Predicted SEE (50)</span>
  <span class="pill">Students at Risk Tab</span>
  <span class="pill">Faculty & Mentor Insights</span>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def train_model():
    np.random.seed(42)
    n_tr = 400
    tr_att = np.random.randint(50, 100, n_tr)
    tr_cie = np.random.uniform(15, 50, n_tr)
    tr_see = np.clip(0.68 * tr_cie + 0.14 * tr_att + np.random.normal(0, 2.0, n_tr), 10, 50)
    return RandomForestRegressor(n_estimators=80, random_state=42).fit(np.column_stack([tr_att, tr_cie]), tr_see)

see_model = train_model()

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
    g_map = {"O":"#dcfce7;color:#166534","A+":"#d1fae5;color:#065f46","A":"#dbeafe;color:#1e40af","B+":"#e0e7ff;color:#3730a3","B":"#fef3c7;color:#92400e","C":"#ffedd5;color:#9a3412","P":"#f3f4f6;color:#374151","F":"#fee2e2;color:#991b1b"}
    return f"background-color:{g_map[val]};font-weight:bold" if val in g_map else ""

def render_personal_dashboard(stu=None):
    if stu:
        if st.button("← Back to All Student Profiles"):
            st.session_state["active_stu"] = None
            st.rerun()
        st.markdown(f"""
        <div class="profile-banner">
          <strong style="color:#312e81;font-size:1.15rem;">360° Student Dashboard: {stu.get('Student Name', 'Student')}</strong><br>
          <span style="color:#6d28d9;font-weight:600;font-size:0.86rem;">USN: {stu.get('USN', '1RN23CS100')} &nbsp;|&nbsp; Status: {stu.get('Status', 'Active')} &nbsp;|&nbsp; Prev Sem Failed Subjects: {int(stu.get('Prev Sem Failed Subjects', 0))}</span>
        </div>
        """, unsafe_allow_html=True)

    tab_acad, tab_place = st.tabs(["Academics & Study Planner", "Skill & Academic Score Growth Plan"])

    with tab_acad:
        eval_mode = st.radio("Internals Completed:", ["Both Internals (1 & 2)", "Only 1st Internal"], horizontal=True)
        only_one = (eval_mode == "Only 1st Internal")

        d_att = int(stu["Attendance (%)"]) if stu and "Attendance (%)" in stu else 84
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

        uid = stu["USN"] if stu and "USN" in stu else "default"
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

        live_df = pd.DataFrame(rows)
        live_res = [get_grade(t, c, s) for t, c, s in zip(live_df["Predicted Total (/100)"], live_df["CIE (/50)"], live_df["Predicted SEE (/50)"])]
        live_df["GP"] = [r[0] for r in live_res]
        live_df["Grade"] = [r[1] for r in live_res]
        live_sgpa = round(float((live_df["Credits"] * live_df["GP"]).sum() / live_df["Credits"].sum()), 2)
        st.session_state[f"pred_sgpa_{uid}"] = live_sgpa

        if st.button("Predict Academics & Generate Study Planner", key=f"btn_ac_{uid}"):
            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Avg", f"{live_df['Predicted Total (/100)'].mean():.1f} / 100")
            m2.metric("Predicted SGPA", f"{live_sgpa:.2f} / 10")
            m3.metric("Subjects Passed", f"{int((live_df['Grade'] != 'F').sum())} / 6")
            st.dataframe(live_df[["Subject", "Credits", "CIE (/50)", "Predicted SEE (/50)", "Predicted Total (/100)", "Grade", "GP"]].style.map(style_grade, subset=["Grade"]), use_container_width=True)
            strengths = live_df[live_df["Predicted Total (/100)"] >= 75]["Subject"].tolist()
            weaknesses = live_df[(live_df["Predicted Total (/100)"] < 60) | (live_df["CIE (/50)"] < 22)]["Subject"].tolist()
            c_sw1, c_sw2 = st.columns(2)
            c_sw1.markdown(f'<div class="sw-box sw-str"><strong>Academic Strengths (&ge;75)</strong><br>{", ".join(strengths) if strengths else "Keep pushing above 75"}</div>', unsafe_allow_html=True)
            c_sw2.markdown(f'<div class="sw-box sw-wk"><strong>Academic Weaknesses (&lt;60)</strong><br>{", ".join(weaknesses) if weaknesses else "No critical subject risk"}</div>', unsafe_allow_html=True)
            plan = [{"Subject": r["Subject"], "Weekly Hours": "8 hrs/wk" if r["Predicted Total (/100)"] < 60 else ("5 hrs/wk" if r["Predicted Total (/100)"] < 75 else "3 hrs/wk"), "Focus": "VTU Past Papers + CIE Recovery" if r["Predicted Total (/100)"] < 60 else "Module Revision + Mock Tests"} for _, r in live_df.iterrows()]
            st.dataframe(pd.DataFrame(plan), use_container_width=True)

    with tab_place:
        st.subheader("How to Maintain & Upgrade Both Skills and Academic Score")
        uid_p = stu["USN"] if stu and "USN" in stu else "default"
        stu_sgpa = st.session_state.get(f"pred_sgpa_{uid_p}", float(stu["SGPA"]) if stu and "SGPA" in stu else 7.55)

        p1, p2 = st.columns(2)
        min_cutoff = p1.number_input("Target Placement Cutoff", 5.0, 9.5, 7.25, 0.25, key=f"pcut_{uid_p}")
        sems_completed = p2.number_input("Semesters Completed", 1, 7, 5, 1, key=f"psem_{uid_p}")

        all_skills = ["Python / Java / C++", "Data Structures & Algorithms", "Full-Stack Web (React/Node)", "SQL & DBMS", "Machine Learning / AI", "Cloud / Docker / Git", "System Design / OS"]
        init_sk = str(stu["Core Skills"]).split(", ") if stu and "Core Skills" in stu else ["Python / Java / C++", "SQL & DBMS"]
        init_sk = [s for s in init_sk if s in all_skills]
        sel_skills = st.multiselect("Current Skills (Select What You Already Know):", all_skills, default=init_sk, key=f"psk_{uid_p}")

        # Dynamic Target Next Sem GPA based on Predicted SGPA, Target Cutoff & Semesters Completed
        rem_sems = max(1, 8 - int(sems_completed))
        req_avg_for_cutoff = ((min_cutoff * 8.0) - (stu_sgpa * int(sems_completed))) / rem_sems
        if stu_sgpa >= min_cutoff:
            target_next_sgpa = round(min(10.0, max(min_cutoff, stu_sgpa + 0.35)), 2)
        else:
            target_next_sgpa = round(min(10.0, max(5.5, req_avg_for_cutoff)), 2)

        step_diff = target_next_sgpa - stu_sgpa
        skill_readiness = int((len(sel_skills) / len(all_skills)) * 100)

        c1, c2 = st.columns(2)
        c1.metric("Target Next Sem GPA", f"{target_next_sgpa:.2f} SGPA", f"{step_diff:+.2f} vs Predicted ({stu_sgpa:.2f})")
        c2.metric("Skill Readiness", f"{skill_readiness}%", f"{len(sel_skills)}/{len(all_skills)} Skills")

        if stu_sgpa >= min_cutoff:
            st.markdown(f'<div class="score-badge">Predicted SGPA ({stu_sgpa:.2f}) clears the {min_cutoff:.2f} cutoff! Target {target_next_sgpa:.2f} SGPA next semester ({step_diff:+.2f} buffer) while building projects, DSA & internships.</div>', unsafe_allow_html=True)
        elif req_avg_for_cutoff > 10.0:
            st.markdown(f'<div class="score-badge">With {stu_sgpa:.2f} SGPA across {int(sems_completed)} semesters, reaching an {min_cutoff:.2f} cumulative cutoff mathematically needs {req_avg_for_cutoff:.2f}/10—so aim for {target_next_sgpa:.2f} SGPA next sem while prioritizing skills for skill-first companies (6.0+ criteria).</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="score-badge">To raise your cumulative GPA from {stu_sgpa:.2f} to the {min_cutoff:.2f} placement cutoff over the remaining {rem_sems} semester(s), target {target_next_sgpa:.2f} SGPA next semester ({step_diff:+.2f} step-up).</div>', unsafe_allow_html=True)

        missing_skills = [s for s in all_skills if s not in sel_skills]
        s_col1, s_col2 = st.columns(2)
        s_col1.markdown("""
        <div class="sw-box sw-str"><strong>1. How to Upgrade Academic Score Steadily</strong><br>
        &bull; Protect CIE first: Aim for 36+/50 in Internals (easiest marks to secure).<br>
        &bull; Zero backlogs rule: Clear weak subjects first before chasing 9+ SGPA.<br>
        &bull; Study 3 past VTU papers per subject 3 weeks before SEE.</div>
        """, unsafe_allow_html=True)
        s_col2.markdown(f"""
        <div class="sw-box sw-wk"><strong>2. How to Upgrade Skills Alongside College</strong><br>
        &bull; Next Skill to Learn: <b>{missing_skills[0] if missing_skills else "System Design & Mock Interviews"}</b>.<br>
        &bull; Daily Habit ({int(sems_completed)}/8 Sems Done): 1 hr DSA/coding + 1 hr project build.<br>
        &bull; Turn college lab mini-projects into GitHub portfolio repos.</div>
        """, unsafe_allow_html=True)

        routine = [
            {"Focus Area": "Academic Maintenance (Protect CIE & Pass All)", "Semesters Completed": f"{int(sems_completed)} / 8", "Concrete Weekly Action": "Revise same-day lecture notes + solve 5 VTU numericals/week"},
            {"Focus Area": "Core Coding & Problem Solving (DSA)", "Semesters Completed": f"{int(sems_completed)} / 8", "Concrete Weekly Action": "Solve 5–7 LeetCode/GFG problems/week in Python/Java/C++"},
            {"Focus Area": f"Skill Upgrade ({missing_skills[0] if missing_skills else 'Full-Stack / AI'})", "Semesters Completed": f"{int(sems_completed)} / 8", "Concrete Weekly Action": "Build 1 working feature/week & push to GitHub for resume proof"}
        ]
        st.dataframe(pd.DataFrame(routine), use_container_width=True)

if st.session_state.get("active_stu") is not None:
    render_personal_dashboard(st.session_state["active_stu"])
else:
    main_tab1, main_tab2, main_tab3 = st.tabs(["1,000-Student Profiles & Cutoff Check", "Students at Risk", "Faculty & Mentor Teaching Insights"])

    with main_tab1:
        st.subheader("Batch Class Analysis (Upload CSV)")
        c_cut1, c_cut2 = st.columns([1.2, 1.8])
        min_batch_cutoff = c_cut1.number_input("Min Cutoff Number:", 5.0, 9.5, 7.0, 0.25)
        up = c_cut2.file_uploader("Upload CSV", type=["csv"])
        if up is not None:
            st.session_state["batch_csv"] = pd.read_csv(up)

        if "batch_csv" in st.session_state:
            bdf = st.session_state["batch_csv"].copy()
            if "Student Name" not in bdf.columns:
                bdf["Student Name"] = [f"Student {i+1}" for i in range(len(bdf))]
            if "USN" not in bdf.columns:
                bdf["USN"] = [f"1RN23CS{100+i}" for i in range(len(bdf))]
            if "Attendance (%)" not in bdf.columns:
                bdf["Attendance (%)"] = 80
            if all(k in bdf.columns for k in ["Internal 1 (/50)", "Internal 2 (/50)"]):
                bdf["CIE (/50)"] = (((bdf["Internal 1 (/50)"] + bdf["Internal 2 (/50)"]) / 100.0) * 50.0).round(1)
            elif "CIE (/50)" not in bdf.columns:
                bdf["CIE (/50)"] = 35.0
            bdf["Predicted SEE (/50)"] = see_model.predict(bdf[["Attendance (%)", "CIE (/50)"]].values).round(1)
            bdf["Predicted Total (/100)"] = (bdf["CIE (/50)"] + bdf["Predicted SEE (/50)"]).round(1)
            bres = [get_grade(t, c, s) for t, c, s in zip(bdf["Predicted Total (/100)"], bdf["CIE (/50)"], bdf["Predicted SEE (/50)"])]
            bdf["SGPA"] = [r[0] for r in bres]
            if "Core Skills" not in bdf.columns:
                bdf["Core Skills"] = "Python / Java / C++, SQL & DBMS"
            if "Prev Sem Failed Subjects" not in bdf.columns:
                bdf["Prev Sem Failed Subjects"] = np.where(bdf["CIE (/50)"] < 20, 2, np.where(bdf["CIE (/50)"] < 23, 1, 0))

            bdf["At Risk"] = (bdf["Prev Sem Failed Subjects"] > 0) | (bdf["SGPA"] < 5.0)
            bdf["Cutoff Gap"] = (bdf["SGPA"] - min_batch_cutoff).round(2)
            bdf["Status"] = np.where(
                bdf["At Risk"],
                "At Risk (Prev Fail / <5 GPA)",
                np.where(bdf["SGPA"] >= min_batch_cutoff, "Eligible (Cutoff Cleared)", "Below Min Cutoff")
            )
            st.session_state["processed_bdf"] = bdf

            eligible_cnt = int((~bdf["At Risk"] & (bdf["SGPA"] >= min_batch_cutoff)).sum())
            at_risk_cnt = int(bdf["At Risk"].sum())

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Students", len(bdf))
            k2.metric("Min Cutoff", f"{min_batch_cutoff:.2f}")
            k3.metric("Crossed Cutoff", f"{eligible_cnt} / {len(bdf)}")
            k4.metric("Students at Risk", f"{at_risk_cnt}")

            st.subheader("Individual Student Profiles")
            q = st.text_input("Search student name or ID", placeholder="e.g., Kavya or 1RN23CS105")
            filtered = bdf[bdf["Student Name"].astype(str).str.contains(q, case=False, na=False) | bdf["USN"].astype(str).str.contains(q, case=False, na=False)] if q else bdf

            grid_cols = st.columns(3)
            for idx, (_, r) in enumerate(filtered.head(9).iterrows()):
                parts = str(r["Student Name"]).split()
                initials = "".join([w[0] for w in parts[:2]]).upper() if parts else "ST"
                tag_cls = "tag-risk" if r["At Risk"] else ("tag-ok" if r["SGPA"] >= min_batch_cutoff else "tag-warn")
                with grid_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="stu-card">
                      <div class="stu-avatar">{initials}</div>
                      <p class="stu-name">{r['Student Name']}</p>
                      <p class="stu-id">ID: {r['USN']} | Prev Fails: {int(r['Prev Sem Failed Subjects'])}</p>
                      <p class="stu-stat">Predicted SGPA: {r['SGPA']} / 10</p>
                      <p class="stu-stat">Cutoff ({min_batch_cutoff}): {r['Cutoff Gap']:+.2f}</p>
                      <span class="{tag_cls}">{r['Status']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Personal Dashboard", key=f"open_{r['USN']}_{idx}"):
                        st.session_state["active_stu"] = r.to_dict()
                        st.rerun()
        else:
            st.divider()
            render_personal_dashboard(None)

    with main_tab2:
        st.subheader("Students at Risk (Failed Previous Sem Subject or GPA < 5.0)")
        pbdf = st.session_state.get("processed_bdf", None)
        if pbdf is not None:
            risk_df = pbdf[pbdf["At Risk"]].copy()
            prev_fail_cnt = int((risk_df["Prev Sem Failed Subjects"] > 0).sum())
            low_gpa_cnt = int((risk_df["SGPA"] < 5.0).sum())

            r1, r2, r3 = st.columns(3)
            r1.metric("Total At-Risk Students", len(risk_df))
            r2.metric("Prev Sem Subject Fails", prev_fail_cnt)
            r3.metric("GPA Less Than 5.0", low_gpa_cnt)

            rq = st.text_input("Search at-risk student name or ID", placeholder="e.g., 1RN23CS112", key="risk_search")
            r_filtered = risk_df[risk_df["Student Name"].astype(str).str.contains(rq, case=False, na=False) | risk_df["USN"].astype(str).str.contains(rq, case=False, na=False)] if rq else risk_df

            r_cols = st.columns(3)
            for idx, (_, r) in enumerate(r_filtered.head(9).iterrows()):
                parts = str(r["Student Name"]).split()
                initials = "".join([w[0] for w in parts[:2]]).upper() if parts else "ST"
                reason = f"Failed {int(r['Prev Sem Failed Subjects'])} Prev Sub" if r["Prev Sem Failed Subjects"] > 0 else "GPA < 5.0"
                with r_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="stu-card">
                      <div class="stu-avatar">{initials}</div>
                      <p class="stu-name">{r['Student Name']}</p>
                      <p class="stu-id">ID: {r['USN']}</p>
                      <p class="stu-stat">SGPA: {r['SGPA']} / 10 | CIE: {r['CIE (/50)']}/50</p>
                      <span class="tag-risk">{reason}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Open Personal Dashboard", key=f"open_risk_{r['USN']}_{idx}"):
                        st.session_state["active_stu"] = r.to_dict()
                        st.rerun()

            st.subheader("Complete At-Risk Student Roster")
            st.dataframe(r_filtered[["USN", "Student Name", "Prev Sem Failed Subjects", "Attendance (%)", "CIE (/50)", "SGPA", "Status"]], use_container_width=True)
        else:
            st.info("Upload your student CSV in the first tab to automatically detect students who failed a previous-semester subject or have GPA < 5.0.")

    with main_tab3:
        st.subheader("Engineering Faculty & Proctor Performance Co-Pilot")
        pbdf = st.session_state.get("processed_bdf", None)
        if pbdf is not None:
            risk_total = int(pbdf["At Risk"].sum())
            low_att = int((pbdf["Attendance (%)"] < 75).sum())
            f1, f2, f3 = st.columns(3)
            f1.metric("Batch Avg CIE", f"{pbdf['CIE (/50)'].mean():.1f} / 50")
            f2.metric("Students at Risk", f"{risk_total} Students")
            f3.metric("Attendance <75%", f"{low_att} Students")
        else:
            st.info("Upload your student CSV in the first tab to see live batch diagnostics alongside these engineering teaching strategies.")

        st.markdown("""
        <div class="fac-card"><strong>1. Problem-First Lectures (Break the 15-Minute Rule)</strong><br>
        Start every engineering module with a real-world system failure or industry use case before deriving equations or algorithms. Pause every 15–20 minutes for a 3-minute live code trace or GATE/VTU 2-mark problem sprint.</div>
        <div class="fac-card"><strong>2. Early Internal-1 Proctor Intervention</strong><br>
        Identify students with previous-semester failed subjects, GPA &lt; 5.0, or CIE &lt; 22/50 immediately. Group them into a 30-minute weekly bridge tutorial before Semester End Exams (SEE) rather than waiting until finals.</div>
        <div class="fac-card"><strong>3. Align Labs & Assignments With Campus Placements</strong><br>
        Replace repetitive record-copying with mini-problem statements, edge-case debugging, 2-minute viva defenses, and GitHub pushes—connecting OS, DBMS, CN, and DSA topics directly to technical interview questions.</div>
        <div class="fac-card"><strong>4. Mid-Semester Anonymous 3-Question Pulse Check</strong><br>
        Run a quick 3-question form after Internal 1 (<i>What clicked? Which module felt rushed? What should change?</i>). Acting on even one student suggestion significantly boosts classroom engagement and trust.</div>
        """, unsafe_allow_html=True)

        if pbdf is not None:
            st.subheader("Priority Proctor Mentoring Queue")
            at_risk_df = pbdf[pbdf["At Risk"] | (pbdf["Attendance (%)"] < 75)][["USN", "Student Name", "Prev Sem Failed Subjects", "Attendance (%)", "CIE (/50)", "SGPA", "Status"]].head(30)
            st.dataframe(at_risk_df, use_container_width=True)
