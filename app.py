import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Page Configuration
st.set_page_config(page_title="Student Performance Insights", page_icon="🎓")
st.title("🎓 Student Performance Insights")
st.markdown("Predict student exam outcomes, identify at-risk learners early, and simulate study interventions.")

# 1. Generate realistic student dataset (200 records)
np.random.seed(42)
n_students = 200
attendance = np.random.randint(50, 100, n_students)
study_hours = np.random.randint(2, 25, n_students)
prev_score = np.random.randint(40, 98, n_students)
assignments = np.random.randint(50, 100, n_students)

# Formula creating realistic correlation + slight noise
final_score = (
    0.30 * attendance +
    1.10 * study_hours +
    0.40 * prev_score +
    0.15 * assignments +
    np.random.normal(0, 3, n_students)
)
final_score = np.clip(final_score, 0, 100)

df = pd.DataFrame({
    "Attendance (%)": attendance,
    "Weekly Study Hours": study_hours,
    "Previous Exam Score": prev_score,
    "Assignment Completion (%)": assignments,
    "Final Score": final_score
})

# 2. Train Model & Calculate Metrics
X = df[["Attendance (%)", "Weekly Study Hours", "Previous Exam Score", "Assignment Completion (%)"]]
y = df["Final Score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

# 3. Display Model Metrics (Matches your existing layout)
st.subheader("📊 Model Performance")
col1, col2 = st.columns(2)
col1.metric("Model MAE (Error)", f"{mae:.2f} Marks")
col2.metric("R² Score (Accuracy)", f"{r2:.2f}")

st.divider()

# 4. Interactive Student Simulator
st.subheader("🔍 Simulate Student Outcome")
in_attendance = st.slider("Attendance (%)", min_value=40, max_value=100, value=78)
in_study = st.slider("Weekly Study Hours", min_value=0, max_value=30, value=10)
in_prev = st.number_input("Previous Exam Score (out of 100)", min_value=0, max_value=100, value=68)
in_assign = st.slider("Assignment Completion (%)", min_value=0, max_value=100, value=85)

if st.button("Analyze Performance"):
    input_data = pd.DataFrame([[in_attendance, in_study, in_prev, in_assign]], columns=X.columns)
    predicted_score = model.predict(input_data)[0]

    st.success(f"**Predicted Final Exam Score:** {predicted_score:.1f} / 100")

    # 5. Actionable Insights Engine
    st.subheader("💡 Recommended Actions")
    if in_attendance < 75:
        st.warning("⚠️ **Attendance Alert:** Below the 75% minimum requirement. Schedule a faculty mentor check-in.")
    if in_study < 8:
        st.info("📚 **Study Plan:** Increasing weekly self-study from current levels to 12+ hours can boost the predicted score by ~5–8 marks.")
    if predicted_score < 50:
        st.error("🚨 **High Academic Risk:** Recommend peer tutoring and remedial weekend sessions.")
    elif predicted_score >= 85:
        st.balloons()
        st.success("🌟 **Top Performer:** Eligible for advanced project tracks or peer-mentorship roles.")
