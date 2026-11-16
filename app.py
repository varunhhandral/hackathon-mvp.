import streamlit as st
import pandas as pd
import numpy as np

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
</style>
<div class="hero">
  <h1>Student Performance Insights</h1>
  <p>AI-Powered RNSIT & VTU Academic Analytics, Integrated CIE + SEE Evaluator & Individual Dashboards</p>
  <span class="pill">CIE (50) + SEE (50) = 100</span>
  <span class="pill">Theory + Lab Scaling</span>
  <span class="pill">1,000-Student Profiles</span>
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
    g_map = {"O":"#dcfce7;color:#166534","A+":"#d1fae5;color:#065f46","A":"#dbeafe;color:#1e40af","B+":"#e0e7ff;color:#3730a3","B":"#fef3c7;color:#92400e","C":"#ffedd5;color:#9a3412","P":"#f3f4f6;color:#374151","F":"#fee2e2;color:#991b1b","At Risk":"#fee2e2;color:#991b1b","On Track":"#dcfce7;color:#166534"}
    return f"background-color:{g_map[val]};font-weight:bold" if val in g_map else ""

cols = ["Attendance (%)", "CIE Marks (/50)", "This Sem Exam (/100)"]

def render_personal_dashboard(stu=None):
    if stu:
        if st.button("← Back to All Student Profiles"):
            st.session_state["active_stu"] = None
            st.rerun()
        st.markdown(f"""
        <div class="profile-banner">
          <strong style="color:#312e81;font-size:1.15rem;">Personal Dashboard: {stu['Student Name']}</strong><br>
          <span style="color:#6d28d9;font-weight:600;font-size:0.88rem;">USN: {stu['USN']} &nbsp;|&nbsp; Status: {stu['Risk']} &nbsp;|&nbsp; Enter or customize 6-subject RNSIT marks below</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.subheader("Personal Dashboard: 6-Subject RNSIT Evaluator")

    g1, g2 = st.columns(2)
    curr_cgpa = g1.number_input("Current CGPA (/10)", 0.0, 10.0, float(stu["Previous CGPA"]) if stu and "Previous CGPA" in stu else 7.65, 0.05)
    comp_sems = g2.number_input("Completed Semesters", 1, 8, 3, 1)

    d_att = int(stu[cols[0]]) if stu else 84
    d_i1 = int(stu["Internal 1 (/50)"]) if stu and "Internal 1 (/50)" in stu else 40
    d_i2 = int(stu["Internal 2 (/50)"]) if stu and "Internal 2 (/50)" in stu else 42
    d_a1 = int(stu["Assignment 1 (/5)"]) if stu and "Assignment 1 (/5)" in stu else 5
    d_a2 = int(stu["Assignment 2 (/5)"]) if stu and "Assignment 2 (/5)" in stu else 4
    d_ts = int(stu[cols[2]]) if stu else 76

    subs_init = [
        ("Data Structures", 4, d_att, d_i1, d_i2, d_a1, d_a2, d_ts, True, 44, 46, True, 42),
        ("Operating Systems", 4, max(60, d_att-6), max(15, d_i1-6), max(16, d_i2-5), d_a1, d_a2, max(45, d_ts-8), True, 38, 40, False, 0),
        ("Database Systems", 4, min(100, d_att+4), min(50, d_i1+3), min(50, d_i2+3), 5, 5, min(98, d_ts+6), True, 45, 48, True, 44),
        ("Computer Networks", 3, max(58, d_att-8), max(14, d_i1-8), max(15, d_i2-7), 3, 4, max(42, d_ts-10), False, 0, 0, False, 0),
        ("Discrete Maths", 4, d_att, max(18, d_i1-2), max(18, d_i2-2), 4, 5, max(48, d_ts-4), False, 0, 0, False, 0),
        ("Software Engg", 3, min(100, d_att+5), min(50, d_i1+4), min(50, d_i2+4), 5, 5, min(98, d_ts+8), False, 0, 0, False, 0)
    ]

    uid = stu["USN"] if stu else "default"
    rows = []
    for i, (nm, cr, at, i1, i2, a1, a2, ts, h_lab, li1, li2, h_ext, ext_m) in enumerate(subs_init):
        with st.expander(f"Subject {i+1}: {nm}", expanded=(i == 0)):
            c_a, c_b = st.columns([3, 1])
            s_nm = c_a.text_input("Subject Name (Editable)", nm, key=f"n_{uid}_{i}")
            s_cr = c_b.number_input("Credits", 1, 6, cr, key=f"c_{uid}_{i}")
            c_c, c_d = st.columns(2)
            s_at = c_c.slider("Attendance (%)", 40, 100, at, key=f"a_{uid}_{i}")
            s_ts = c_d.number_input("This Sem Exam Final (/100)", 0, 100, ts, key=f"ts_{uid}_{i}")
            k1, k2, k3, k4 = st.columns(4)
            v1 = k1.number_input("Theory Int 1 (/50)", 0, 50, i1, key=f"i1_{uid}_{i}")
            v2 = k2.number_input("Theory Int 2 (/50)", 0, 50, i2, key=f"i2_{uid}_{i}")
            v3 = k3.number_input("Assign 1 (/5)", 0, 5, a1, key=f"a1_{uid}_{i}")
            v4 = k4.number_input("Assign 2 (/5)", 0, 5, a2, key=f"a2_{uid}_{i}")
            has_lab = st.checkbox("Include Lab Component?", value=h_lab, key=f"hl_{uid}_{i}")
            if has_lab:
                l1, l2, l3 = st.columns(3)
                lv1 = l1.number_input("Lab Int 1 (/50)", 0, 50, li1, key=f"li1_{uid}_{i}")
                lv2 = l2.number_input("Lab Int 2 (/50)", 0, 50, li2, key=f"li2_{uid}_{i}")
                has_ext = l3.checkbox("External Lab Exam?", value=h_ext, key=f"he_{uid}_{i}")
                ext_val = st.number_input("External Lab (/50)", 0, 50, ext_m if ext_m > 0 else 40, key=f"ex_{uid}_{i}") if has_ext else 0
                cie_val = round(((v1 + v2) / 100.0) * 25.0 + ((v3 + v4) / 10.0) * 5.0 + ((lv1 + lv2) / 100.0) * 20.0, 1)
                see_val = round((s_ts / 100.0) * 35.0 + (ext_val / 50.0) * 15.0, 1) if has_ext else round(s_ts * 0.5, 1)
            else:
                cie_val = round(((v1 + v2) / 100.0) * 40.0 + v3 + v4, 1)
                see_val = round(s_ts * 0.5, 1)
            tot_val = round(cie_val + see_val, 1)
            st.markdown(f'<div class="score-badge">Scaled CIE: {cie_val}/50 &nbsp;|&nbsp; Scaled SEE: {see_val}/50 &nbsp;|&nbsp; Final Total: {tot_val}/100</div>', unsafe_allow_html=True)
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
        show_s = sdf[["Subject", "Credits", cols[1], "SEE (/50)", "Final Total (/100)", "Grade", "GP"]]
        st.dataframe(show_s.style.map(style_grade, subset=["Grade"]), use_container_width=True)
        if stu:
            st.text_area("Mentor Summary for Student", f"Student: {stu['Student Name']} ({stu['USN']})\nSemester SGPA: {sgpa:.2f} | Projected CGPA: {ncgpa:.2f}\nAverage Score: {sdf['Final Total (/100)'].mean():.1f}/100", height=165)

# Route View: Inside Personal Dashboard vs Batch Class & Student Profiles
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
        "This Sem Exam (/100)": np.random.randint(38, 98, ns),
        "Previous CGPA": np.round(np.random.uniform(5.8, 9.6, ns), 2)
    })
    st.download_button("Download 1,000-Student Dataset (CSV)", samp.to_csv(index=False).encode(), "rnsit_1000_students.csv", "text/csv")

    up = st.file_uploader("Upload CSV", type=["csv"])
    if up is not None:
        st.session_state["batch_csv"] = pd.read_csv(up)

    if "batch_csv" in st.session_state:
        bdf = st.session_state["batch_csv"].copy()
        if "Last Sem Exam (/100)" in bdf.columns and cols[2] not in bdf.columns:
            bdf = bdf.rename(columns={"Last Sem Exam (/100)": cols[2]})
        if "USN" not in bdf.columns:
            bdf["USN"] = [f"1RN23CS{100+i}" for i in range(len(bdf))]
        if all(k in bdf.columns for k in ["Internal 1 (/50)", "Internal 2 (/50)", "Assignment 1 (/5)", "Assignment 2 (/5)"]):
            bdf[cols[1]] = (((bdf["Internal 1 (/50)"] + bdf["Internal 2 (/50)"]) / 100.0) * 40.0 + bdf["Assignment 1 (/5)"] + bdf["Assignment 2 (/5)"]).round(1)
        bdf["SEE (/50)"] = (bdf[cols[2]] * 0.5).round(1)
        bdf["Final Total (/100)"] = (bdf[cols[1]] + bdf["SEE (/50)"]).round(1)
        bres = [get_grade(t, c, s) for t, c, s in zip(bdf["Final Total (/100)"], bdf[cols[1]], bdf["SEE (/50)"])]
        bdf["SGPA"] = [r[0] for r in bres]
        bdf["Grade"] = [r[1] for r in bres]
        base_c = bdf["Previous CGPA"] if "Previous CGPA" in bdf.columns else (bdf[cols[2]] / 10.0)
        bdf["Projected CGPA"] = (((base_c * 3) + bdf["SGPA"]) / 4).round(2)
        bdf["Pass Prob (%)"] = np.clip((bdf["Final Total (/100)"] * 1.45 + bdf[cols[0]] * 0.25), 12.0, 100.0).round(2)
        bdf["Risk"] = np.where((bdf[cols[1]] < 20) | (bdf[cols[0]] < 75) | (bdf["Final Total (/100)"] < 45), "At Risk", "On Track")

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Students", len(bdf))
        k2.metric("Avg Total", f"{bdf['Final Total (/100)'].mean():.1f}")
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
                  <p class="stu-stat">Predicted Marks: {r['Final Total (/100)']}</p>
                  <p class="stu-stat">Pass Probability: {r['Pass Prob (%)']}%</p>
                  <span class="{tag_cls}">{r['Risk']}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Open Personal Dashboard", key=f"open_{r['USN']}_{idx}"):
                    st.session_state["active_stu"] = r.to_dict()
                    st.rerun()

        with st.expander("View Full 1,000-Student Table & Download Report"):
            flt = st.radio("Filter:", ["All", "At-Risk Only"], horizontal=True)
            disp = bdf[bdf["Risk"] == "At Risk"] if flt == "At-Risk Only" else bdf
            st.dataframe(disp.style.map(style_grade, subset=["Grade", "Risk"]), use_container_width=True)
            st.download_button("Download Report (CSV)", bdf.to_csv(index=False).encode(), "rnsit_report.csv", "text/csv")
    else:
        st.divider()
        render_personal_dashboard(None)
