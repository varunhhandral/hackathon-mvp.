import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Page Configuration
st.set_page_config(page_title="Student Performance Insights", layout="centered")
st.title("Student Performance Insights")
st.markdown("Predict student exam outcomes, identify at-risk learners early, and simulate study interventions.")

# 1. Generate realistic training dataset (200 records)
np.random.seed(42)
n_students = 200
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

# 3. Display Model Metrics
st.subheader("Model Performance")
col1, col2 = st.columns(2)
col1.metric("Model MAE (Error)", f"{mean_absolute_error(y_test, preds):.2f} Marks")
col2.metric("R2 Score (Accuracy)", f"{r2_score(y_test, preds):.2f}")

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

# 5. Batch Class Analysis (CSV Upload)
st.subheader("Batch Class Analysis (Upload CSV)")
st.markdown("Upload a student roster CSV to predict scores for the whole class and flag at-risk students.")

# Generate 1,000 realistic student records for instant CSV download
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

    if all(col in batch_df.columns for col in feature_cols):
        batch_df["Predicted Final Score"] = model.predict(batch_df[feature_cols]).round(1)
        batch_df["Risk Status"] = np.where(
            (batch_df["Predicted Final Score"] < 55) | (batch_df["Attendance (%)"] < 75),
            "At Risk",
            "On Track"
        )

        at_risk_count = (batch_df["Risk Status"] == "At Risk").sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Students", len(batch_df))
        c2.metric("Class Avg Score", f"{batch_df['Predicted Final Score'].mean():.1f}")
        c3.metric("At-Risk Students", f"{at_risk_count}")

        st.dataframe(batch_df, use_container_width=True)

        st.download_button(
            label="Download Analyzed Report (CSV)",
            data=batch_df.to_csv(index=False).encode("utf-8"),
            file_name="student_performance_report.csv",
            mime="text/csv"
        )
    else:
        st.error(f"CSV must include these exact columns: {', '.join(feature_cols)}")
