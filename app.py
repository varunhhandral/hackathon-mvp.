import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Page Configuration
st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("Predict student exam outcomes, identify root causes for at-risk learners, and generate 30-day intervention plans.")

# 1. Generate realistic training dataset (250 records)
np.random.seed(42)
n_students = 250
attendance = np.random.randint(50, 100, n_students)
study_hours = np.random.randint(2, 25, n_students)
prev_score = np.random.randint(40, 98, n_students)
assignments = np.random.randint(50, 100, n_students)

final_score = np.clip(
    0.30 * attendance + 1.10 * study_hours + 0.40 * prev_score + 0.15 * assignments + np.random.normal(0, 3, n_students),
    0, 100
)

df = pd.DataFrame({
    "Attendance (%)": attendance,
    "Weekly Study Hours": study_hours,
    "Previous Exam Score": prev_score,
    "Assignment Completion (%)": assignments,
    "Final Score": final_score
})

# 2. Train Model & Calculate Metrics
feature_cols = ["Attendance (%)", "Weekly Study Hours", "Previous Exam Score", "Assignment Completion (%)"]
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

# 4. Interactive Single-Student Simulator
st.subheader("Simulate Individual Student Outcome")
in_attendance = st.slider("Attendance (%)", min_value=40, max_value=100, value=78)
in_study = st.slider("Weekly Study Hours", min_value=0, max_value=30, value=10)
in_prev = st.number_input("Previous Exam Score (out of 100)", min_value=0, max_value=100, value=68)
in_assign = st.slider("Assignment Completion (%)", min_value=0, max_value=100, value=85)

if st.button("Analyze Performance"):
    input_data = pd.DataFrame([[in_attendance, in_study, in_prev, in_assign]], columns=feature_cols)
    predicted_score = model.predict(input_data)[0]

    st.success(f"Predicted Final Exam Score: {predicted_score:.1f} / 100")

    st.subheader("Recommended Actions")
    if in_attendance < 75:
        st.warning("Attendance Alert: Below the 75% minimum requirement. Schedule a faculty mentor check-in.")
    if in_study < 8:
        st.info("Study Plan: Increasing weekly self-study to 12+ hours can boost the predicted score by ~5-8 marks.")
    if predicted_score < 50:
        st.error("High Academic Risk: Recommend peer tutoring and remedial weekend sessions.")
    elif predicted_score >= 85:
        st.balloons()
        st.success("Top Performer: Eligible for advanced project tracks or peer-mentorship roles.")

st.divider()

# 5. Batch Class Analysis (CSV Upload + Smart Column Mapper)
st.subheader("Batch Class Analysis (Upload CSV)")
st.markdown("Upload any student roster CSV to predict scores, visualize class distribution, and generate intervention plans.")

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
    "Weekly Study Hours": np.random.randint(1, 26, n_sample),
    "Previous Exam Score": np.random.randint(35, 99, n_sample),
    "Assignment Completion (%)": np.random.randint(45, 100, n_sample)
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

    # Smart Column Mapper if external CSV headers do not match exact names
    if not all(col in batch_df.columns for col in feature_cols):
        st.info("Custom CSV detected. Map your columns to the model inputs below:")
        cols = list(batch_df.columns)
        m1, m2 = st.columns(2)
        map_att = m1.selectbox("Attendance Column", cols, index=0)
        map_study = m2.selectbox("Study Hours Column", cols, index=min(1, len(cols) - 1))
        map_prev = m1.selectbox("Previous Score Column", cols, index=min(2, len(cols) - 1))
        map_assign = m2.selectbox("Assignments Column", cols, index=min(3, len(cols) - 1))

        batch_df = batch_df.rename(columns={
            map_att: "Attendance (%)",
            map_study: "Weekly Study Hours",
            map_prev: "Previous Exam Score",
            map_assign: "Assignment Completion (%)"
        })

    # Run Predictions & Root-Cause Tagging
    batch_df["Predicted Final Score"] = model.predict(batch_df[feature_cols]).round(1)
    batch_df["Risk Status"] = np.where(
        (batch_df["Predicted Final Score"] < 55) | (batch_df["Attendance (%)"] < 75),
        "At Risk",
        "On Track"
    )

    def get_primary_risk(row):
        if row["Attendance (%)"] < 75:
            return "Low Attendance (<75%)"
        elif row["Weekly Study Hours"] < 6:
            return "Low Study Hours (<6h)"
        elif row["Previous Exam Score"] < 55:
            return "Weak Foundation (<55)"
        elif row["Assignment Completion (%)"] < 65:
            return "Missed Assignments"
        elif row["Predicted Final Score"] < 55:
            return "Overall Borderline"
        return "None"

    batch_df["Primary Risk Factor"] = batch_df.apply(get_primary_risk, axis=1)

    # Class Summary KPIs
    at_risk_count = (batch_df["Risk Status"] == "At Risk").sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Students", len(batch_df))
    c2.metric("Class Avg Score", f"{batch_df['Predicted Final Score'].mean():.1f}")
    c3.metric("At-Risk Students", f"{at_risk_count}")

    # Visual Grade Distribution Chart
    bins = [0, 50, 75, 100]
    labels = ["Fail (<50)", "Average (50-75)", "Distinction (>75)"]
    grade_dist = pd.cut(batch_df["Predicted Final Score"], bins=bins, labels=labels).value_counts().reindex(labels)
    st.markdown("**Class Score Distribution**")
    st.bar_chart(grade_dist)

    # Interactive Roster Filter
    filter_option = st.radio("Filter Student Roster:", ["All Students", "At-Risk Only"], horizontal=True)
    display_df = batch_df[batch_df["Risk Status"] == "At Risk"] if filter_option == "At-Risk Only" else batch_df

    st.dataframe(display_df, use_container_width=True)

    st.download_button(
        label="Download Analyzed Report (CSV)",
        data=batch_df.to_csv(index=False).encode("utf-8"),
        file_name="student_performance_report.csv",
        mime="text/csv"
    )

    # 6. Automated Mentor Action Plan & Goal Seeker
    st.divider()
    st.subheader("Automated Mentor Action Plan & Goal Seeker")

    if "Student Name" not in batch_df.columns:
        batch_df["Student Name"] = [f"Student {i + 1}" for i in range(len(batch_df))]

    selected_student = st.selectbox("Select a student to generate a 30-day intervention plan:", batch_df["Student Name"].head(100))
    s_row = batch_df[batch_df["Student Name"] == selected_student].iloc[0]

    target_score = st.slider("Target Score Goal", min_value=50, max_value=95, value=75)
    gap = max(0.0, target_score - s_row["Predicted Final Score"])
    extra_hours = round(gap / 1.1, 1)

    st.text_area(
        "Ready-to-Send Mentor / Parent Summary",
        value=(
            f"Student: {selected_student}\n"
            f"Current Predicted Score: {s_row['Predicted Final Score']}/100 ({s_row['Risk Status']})\n"
            f"Primary Risk Factor: {s_row['Primary Risk Factor']}\n\n"
            f"Recommended 30-Day Action Plan to reach {target_score}/100:\n"
            f"1. Maintain attendance above 80% (Currently: {s_row['Attendance (%)']}%).\n"
            f"2. Add +{extra_hours} weekly self-study hours (Currently: {s_row['Weekly Study Hours']} hrs/wk).\n"
            f"3. Complete pending coursework to reach 90%+ assignment completion (Currently: {s_row['Assignment Completion (%)']}%)."
        ),
        height=195
    )
