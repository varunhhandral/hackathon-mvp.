import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("RNSIT / VTU Scheme: **CIE (50 Marks)** [2 Internals + 2 Assignments] + **Predicted SEE (50 Marks)** = **Total (100)**, SGPA & CGPA.")

def get_gpa_and_grade(total_score, cie_marks, see_marks):
    if cie_marks < 20 or see_marks < 18 or total_score < 40:
        return 0.0, "F"
    elif total_score >= 90:
        return 10.0, "O"
    elif total_score >= 80:
        return 9.0, "A+"
    elif total_score >= 70:
        return 8.0, "A"
    elif total_score >= 60:
        return 7.0, "B+"
    elif total_score >= 55:
        return 6.0, "B"
    elif total_score >= 50:
        return 5.0, "C"
    else:
        return 4.0, "P"

# 1. Generate realistic RNSIT/VTU training dataset
np.random.seed(42)
n_students = 300
attendance = np.random.randint(55, 100, n_students)
cie_total = np.random.uniform(18, 50, n_students)
last_sem_exam = np.random.randint(35, 98, n_students)

see_score = np.clip(
    0.45 * cie_total + 0.18 * last_sem_exam + 0.12 * attendance + np.random.normal(0, 2.2, n_students),
    0, 50
)

df = pd.DataFrame({
    "Attendance (%)": attendance,
    "CIE Marks (out of 50)": cie_total,
    "Last Sem Exam (out of 100)": last_sem_exam,
    "SEE Marks (out of 50)": see_score
})

# 2. Train Model
feature_cols = ["Attendance (%)", "CIE Marks (out of 50)", "Last Sem Exam (out of 100)"]
X = df[feature_cols]
y = df["SEE Marks (out of 50)"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

# 3. Display Model Metrics
st.subheader("Model Performance & Key Drivers (SEE Prediction)")
col1, col2 = st.columns(2)
col1.metric("SEE Model MAE (Error)", f"{mean_absolute_error(y_test, preds):.2f} / 50 Marks")
col2.metric("R2 Score (Accuracy)", f"{r2_score(y_test, preds):.2f}")

importance_df = pd.DataFrame({
    "Factor": feature_cols,
    "Impact": model.feature_importances_
}).sort_values(by="Impact", ascending=True)
st.caption("Feature Importance: What drives Semester End Exam (SEE) marks most")
st.bar_chart(importance_df.set_index("Factor"))

st.divider()

# 4. Interactive 6-Subject RNSIT/VTU Simulator
st.subheader("Simulate 6-Subject Semester Outcome (RNSIT Scheme)")
st.markdown("Enter **2 Internals (out of 50)**, **2 Assignments (out of 5)**, **Attendance (%)**, and **Last Sem Exam (out of 100)** for all 6 subjects.")

c_gpa1, c_gpa2 = st.columns(2)
current_cgpa = c_gpa1.number_input("Current CGPA (out of 10)", min_value=0.0, max_value=10.0, value=7.65, step=0.05)
completed_sems = c_gpa2.number_input("Completed Semesters", min_value=1, max_value=8, value=3, step=1)

default_subjects = [
    ("Data Structures & Applications", 4, 86, 41, 43, 5, 4, 78),
    ("Operating Systems", 4, 72, 24, 26, 4, 3, 62),
    ("Database Management Systems", 4, 90, 44, 46, 5, 5, 84),
    ("Computer Networks", 3, 68, 18, 20, 3, 3, 54),
    ("Discrete Mathematical Structures", 4, 80, 36, 38, 4, 5, 72),
    ("Software Engineering & Testing", 3, 92, 45, 47, 5, 5, 86)
]

subject_inputs = []
for i, (def_name, def_cred, def_att, def_i1, def_i2, def_a1, def_a2, def_last) in enumerate(default_subjects):
    with st.expander(f"Subject {i + 1}: {def_name}", expanded=(i == 0)):
        s_col1, s_col2 = st.columns([3, 1])
        s_name = s_col1.text_input("Subject Name", value=def_name, key=f"name_{i}")
        s_cred = s_col2.number_input("Credits", min_value=1, max_value=6, value=def_cred, key=f"cred_{i}")

        r1_c1, r1_c2 = st.columns(2)
        s_att = r1_c1.slider("Attendance (%)", 40, 100, def_att, key=f"att_{i}")
        s_last = r1_c2.number_input("Last Sem Exam (out of 100)", 0, 100, def_last, key=f"last_{i}")

        st.caption("Continuous Internal Evaluation (CIE - Total 50 Marks)")
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        s_int1 = r2_c1.number_input("Internal 1 (/50)", 0, 50, def_i1, key=f"int1_{i}")
        s_int2 = r2_c2.number_input("Internal 2 (/50)", 0, 50, def_i2, key=f"int2_{i}")
        s_asg1 = r2_c3.number_input("Assign 1 (/5)", 0, 5, def_a1, key=f"asg1_{i}")
        s_asg2 = r2_c4.number_input("Assign 2 (/5)", 0, 5, def_a2, key=f"asg2_{i}")

        int_scaled = round(((s_int1 + s_int2) / 100.0) * 40.0, 1)
        asg_total = s_asg1 + s_asg2
        cie_calc = round(int_scaled + asg_total, 1)
        st.info(f"Calculated CIE: {cie_calc} / 50 (Internals: {int_scaled}/40 + Assignments: {asg_total}/10)")

        subject_inputs.append({
            "Subject": s_name,
            "Credits": s_cred,
            "Attendance (%)": s_att,
            "CIE Marks (out of 50)": cie_calc,
            "Last Sem Exam (out of 100)": s_last
        })

if st.button("Predict SEE, Final Total (100), SGPA & CGPA"):
    sub_df = pd.DataFrame(subject_inputs)
    sub_df["Predicted SEE (/50)"] = model.predict(sub_df[feature_cols]).round(1)
    sub_df["Final Total (/100)"] = (sub_df["CIE Marks (out of 50)"] + sub_df["Predicted SEE (/50)"]).round(1)

    gpa_info = [
        get_gpa_and_grade(tot, cie, see)
        for tot, cie, see in zip(
            sub_df["Final Total (/100)"],
            sub_df["CIE Marks (out of 50)"],
            sub_df["Predicted SEE (/50)"]
        )
    ]
    sub_df["Grade Point"] = [g[0] for g in gpa_info]
    sub_df["Grade"] = [g[1] for g in gpa_info]
    sub_df["Credit Points"] = sub_df["Credits"] * sub_df["Grade Point"]

    total_credits = sub_df["Credits"].sum()
    sem_sgpa = sub_df["Credit Points"].sum() / total_credits
    new_cgpa = ((current_cgpa * completed_sems) + sem_sgpa) / (completed_sems + 1)
    cgpa_delta = new_cgpa - current_cgpa
    avg_total = sub_df["Final Total (/100)"].mean()

    m1, m2, m3 = st
