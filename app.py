import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Page Configuration
st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("Predict multi-subject student exam outcomes, calculate credit-weighted SGPA & CGPA, and generate 30-day intervention plans.")

# Helper function: Convert 0-100 score to 10-point Grade Point & Letter Grade
def get_gpa_and_grade(score):
    if score >= 90:
        return 10.0, "O"
    elif score >= 80:
        return 9.0, "A+"
    elif score >= 70:
        return 8.0, "A"
    elif score >= 60:
        return 7.0, "B+"
    elif score >= 55:
        return 6.0, "B"
    elif score >= 50:
        return 5.0, "C"
    else:
        return 0.0, "F"

# 1. Generate realistic training dataset (250 records)
np.random.seed(42)
n_students = 250
attendance = np.random.randint(50, 100, n_students)
prev_score = np.random.randint(40, 98, n_students)
assignments = np.random.randint(50, 100, n_students)

final_score = np.clip(
    0.35 * attendance + 0.45 * prev_score + 0.20 * assignments + np.random.normal(0, 3, n_students),
    0, 100
)

df = pd.DataFrame({
    "Attendance (%)": attendance,
    "Previous Exam Score": prev_score,
    "Assignment Completion (%)": assignments,
    "Final Score": final_score
})

# 2. Train Model & Calculate Metrics
feature_cols = ["Attendance (%)", "Previous Exam Score", "Assignment Completion (%)"]
X = df[feature_cols]
y = df["Final Score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

# 3. Display Model Metrics & Explainable AI (Feature Importance)
st.subheader("Model Performance & Key Drivers")
col1, col2 = st.columns(2)
col1.metric("Model MAE (Error)", f"{mean_absolute_error(y_test, preds):.2f} Marks")
col2.metric("R2 Score (Accuracy)", f"{r2_score(y_test, preds):.2f}")

importance_df = pd.DataFrame({
    "Factor": feature_cols,
    "Impact": model.feature_importances_
}).sort_values(by="Impact", ascending=True)
st.caption("Feature Importance: What drives final exam scores most")
st.bar_chart(importance_df.set_index("Factor"))

st.divider()

# 4. Interactive 6-Subject Student Simulator + Credit-Weighted SGPA & CGPA
st.subheader("Simulate 6-Subject Semester Outcome & CGPA")
st.markdown("Enter details for all **6 subjects** below to predict subject-wise marks, credit-weighted SGPA, and updated CGPA.")

c_gpa1, c_gpa2 = st.columns(2)
current_cgpa = c_gpa1.number_input("Current CGPA (out of 10)", min_value=0.0, max_value=10.0, value=7.40, step=0.1)
completed_sems = c_gpa2.number_input("Completed Semesters", min_value=1, max_value=8, value=2, step=1)

default_subjects = [
    ("Data Structures", 4, 84, 76, 88),
    ("Operating Systems", 4, 72, 64, 75),
    ("Database Management", 4, 88, 82, 92),
    ("Computer Networks", 3, 68, 58, 70),
    ("Discrete Mathematics", 4, 79, 71, 80),
    ("Software Engineering Lab", 2, 92, 85, 95)
]

subject_inputs = []
for i, (def_name, def_cred, def_att, def_prev, def_assign) in enumerate(default_subjects):
    with st.expander(f"Subject {i + 1}: {def_name}", expanded=(i == 0)):
        s_col1, s_col2 = st.columns([3, 1])
        s_name = s_col1.text_input("Subject Name", value=def_name, key=f"name_{i}")
        s_cred = s_col2.number_input("Credits", min_value=1, max_value=6, value=def_cred, key=f"cred_{i}")

        m_col1, m_col2, m_col3 = st.columns(3)
        s_att = m_col1.slider("Attendance (%)", 40, 100, def_att, key=f"att_{i}")
        s_prev = m_col2.number_input("Prev Score", 0, 100, def_prev, key=f"prev_{i}")
        s_assign = m_col3.slider("Assignments (%)", 0, 100, def_assign, key=f"assign_{i}")

        subject_inputs.append({
            "Subject": s_name,
            "Credits": s_cred,
            "Attendance (%)": s_att,
            "Previous Exam Score": s_prev,
            "Assignment Completion (%)": s_assign
        })

if st.button("Analyze All 6 Subjects & CGPA"):
    sub_df = pd.DataFrame(subject_inputs)
    sub_df["Predicted Score"] = model.predict(sub_df[feature_cols]).round(1)

    gpa_info = sub_df["Predicted Score"].apply(get_gpa_and_grade)
    sub_df["Grade Point"] = [g[0] for g in gpa_info]
    sub_df["Grade"] = [g[1] for g in gpa_info]
    sub_df["Credit Points"] = sub_df["Credits"] * sub_df["Grade Point"]

    total_credits = sub_df["Credits"].sum()
    sem_sgpa = sub_df["Credit Points"].sum() / total_credits
    new_cgpa = ((current_cgpa * completed_sems) + sem_sgpa) / (completed_sems + 1)
    cgpa_delta = new_cgpa - current_cgpa
    avg_score = sub_df["Predicted Score"].mean()

    m1, m2, m3 = st.columns(3)
    m1.metric("Semester Avg Score", f"{avg_score:.1f} / 100")
    m2.metric("Credit-Weighted SGPA", f"{sem_sgpa:.2f} / 10")
    m3.metric("Projected CGPA", f"{new_cgpa:.2f} / 10", f"{cgpa_delta:+.2f}")

    st.dataframe(
        sub_df[["Subject", "Credits", "Attendance (%)", "Predicted Score", "Grade", "Grade Point"]],
        use_container_width=True
    )

    # Subject-Specific Recommended Actions
    st.subheader("Subject-Wise Recommended Actions")
    low_att_subs = sub_df[sub_df["Attendance (%)"] < 75]["Subject"].tolist()
    weak_subs = sub_df[sub_df["Predicted Score"] < 60]["Subject"].tolist()
    low_assign_subs = sub_df[sub_df["Assignment Completion (%)"] < 75]["Subject"].tolist()

    if low_att_subs:
        st.warning(f"Attendance Shortage (<75%) in: {', '.join(low_att_subs)}. Prioritize classes immediately to avoid exam debarment.")
    if weak_subs:
        st.error(f"High Academic Risk (<60 marks) in: {', '.join(weak_subs)}. Schedule faculty mentor tutoring.")
    if low_assign_subs:
        st.info(f"Pending Assignments (<75%) in: {', '.join(low_assign_subs)}. Completing coursework can add +4 to 6 marks.")
    if not low_att_subs and not weak_subs and not low_assign_subs:
        st.balloons()
        st.success("All 6 subjects are on track! Eligible for honours projects or peer mentorship.")

st.divider()

# 5. Batch Class Analysis (CSV Upload + Smart Column Mapper + GPA/CGPA)
st.subheader("Batch Class Analysis (Upload CSV)")
st.markdown("Upload any student roster CSV to predict scores, compute SGPA & CGPA, and generate intervention plans.")

np.random.seed(99)
n_sample = 1000
first_names = ["Aarav", "Diya", "Rohan", "Meera", "Kabir", "Ananya", "Vikram", "Priya", "Arjun", "Sneha",
               "Rahul", "Kavya", "Aditya", "Neha", "Siddharth", "Pooja", "Karan", "Ishita", "Varun", "Riya"]
last_names = ["Sharma", "Patel", "Reddy", "Nair", "Verma", "Gupta", "Iyer", "Singh", "Kumar", "Joshi",
              "Das", "Mehta", "Bose", "Rao", "Pillai", "Choudhury", "Malhotra", "Bhat", "Menon", "Kulkarni"]

student_names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)} ({1001 + i})" for i in range(n_sample)]

sample_df = pd.DataFrame({
    "Student Name": student_names,
    "Attendance (%)": np.random.randint(48, 100, n_sample),
    "Previous Exam Score": np.random.randint(35, 99, n_sample),
    "Assignment Completion (%)": np.random.randint(45, 100, n_sample),
    "Previous CGPA": np.round(np.random.uniform(5.2, 9.6, n_sample), 2)
})

st.download_button(
    label="Download 1,000-Student Dataset (CSV)",
    data=sample_df.to_csv(index=False).encode("utf-8"),
    file_name="1000_students_dataset.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    batch_df = pd.read_csv(uploaded_file)

    if not all(col in batch_df.columns for col in feature_cols):
        st.info("Custom CSV detected. Map your columns to the model inputs below:")
        cols = list(batch_df.columns)
        m1, m2, m3 = st.columns(3)
        map_att = m1.selectbox("Attendance Column", cols, index=0)
        map_prev = m2.selectbox("Previous Score Column", cols, index=min(1, len(cols) - 1))
        map_assign = m3.selectbox("Assignments Column", cols, index=min(2, len(cols) - 1))

        batch_df = batch_df.rename(columns={
            map_att: "Attendance (%)",
            map_prev: "Previous Exam Score",
            map_assign: "Assignment Completion (%)"
        })

    batch_df["Predicted Final Score"] = model.predict(batch_df[feature_cols]).round(1)
    gpa_results = batch_df["Predicted Final Score"].apply(get_gpa_and_grade)
    batch_df["Predicted SGPA"] = [res[0] for res in gpa_results]
    batch_df["Grade"] = [res[1] for res in gpa_results]

    if "Previous CGPA" in batch_df.columns:
        base_cgpa = batch_df["Previous CGPA"]
    else:
        base_cgpa = (batch_df["Previous Exam Score"] / 10.0).round(2)

    batch_df["Projected CGPA"] = (((base_cgpa * 3) + batch_df["Predicted SGPA"]) / 4).round(2)

    batch_df["Risk Status"] = np.where(
        (batch_df["Predicted Final Score"] < 55) | (batch_df["Attendance (%)"] < 75),
        "At Risk",
        "On Track"
    )

    def get_primary_risk(row):
        if row["Attendance (%)"] < 75:
            return "Low Attendance (<75%)"
        elif row["Previous Exam Score"] < 55:
            return "Weak Foundation (<55)"
        elif row["Assignment Completion (%)"] < 65:
            return "Missed Assignments"
        elif row["Predicted Final Score"] < 55:
            return "Overall Borderline"
        return "None"

    batch_df["Primary Risk Factor"] = batch_df.apply(get_primary_risk, axis=1)

    at_risk_count = (batch_df["Risk Status"] == "At Risk").sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", len(batch_df))
    c2.metric("Class Avg Score", f"{batch_df['Predicted Final Score'].mean():.1f}")
    c3.metric("Avg Class CGPA", f"{batch_df['Projected CGPA'].mean():.2f}")
    c4.metric("At-Risk Students", f"{at_risk_count}")

    bins = [0, 50, 75, 100]
    labels = ["Fail (<50)", "Average (50-75)", "Distinction (>75)"]
    grade_dist = pd.cut(batch_df["Predicted Final Score"], bins=bins, labels=labels).value_counts().reindex(labels)
    st.markdown("**Class Score Distribution**")
    st.bar_chart(grade_dist)

    filter_option = st.radio("Filter Student Roster:", ["All Students", "At-Risk Only"], horizontal=True)
    display_df = batch_df[batch_df["Risk Status"] == "At Risk"] if filter_option == "At-Risk Only" else batch_df

    st.dataframe(display_df, use_container_width=True)

    st.download_button(
        label="Download Analyzed Report (CSV)",
        data=batch_df.to_csv(index=False).encode("utf-8"),
        file_name="student_performance_report.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("Automated Mentor Action Plan & Goal Seeker")

    if "Student Name" not in batch_df.columns:
        batch_df["Student Name"] = [f"Student {i + 1}" for i in range(len(batch_df))]

    selected_student = st.selectbox("Select a student to generate a 30-day intervention plan:", batch_df["Student Name"].head(100))
    s_row = batch_df[batch_df["Student Name"] == selected_student].iloc[0]

    target_score = st.slider("Target Score Goal", min_value=50, max_value=95, value=75)
    gap = max(0.0, target_score - s_row["Predicted Final Score"])
    attendance_boost = min(100, int(s_row["Attendance (%)"] + round(gap / 0.35)))

    st.text_area(
        "Ready-to-Send Mentor / Parent Summary",
        value=(
            f"Student: {selected_student}\n"
            f"Current Predicted Score: {s_row['Predicted Final Score']}/100 | SGPA: {s_row['Predicted SGPA']} | Projected CGPA: {s_row['Projected CGPA']} ({s_row['Risk Status']})\n"
            f"Primary Risk Factor: {s_row['Primary Risk Factor']}\n\n"
            f"Recommended 30-Day Action Plan to reach {target_score}/100:\n"
            f"1. Target attendance of {max(80, attendance_boost)}% (Currently: {s_row['Attendance (%)']}%).\n"
            f"2. Complete pending coursework to reach 90%+ assignment completion (Currently: {s_row['Assignment Completion (%)']}%).\n"
            f"3. Schedule weekly mentor revision check-ins to bridge the {gap:.1f}-mark gap."
        ),
        height=205
    )
