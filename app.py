import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

st.markdown("---")
st.subheader("🤖 Predictive Analytics (House Price Model)")

# Sample training data from your teammate's script
train_data = {
    "area": [600, 800, 1000, 1200, 1500, 1800, 2000],
    "bedrooms": [1, 2, 2, 3, 3, 3, 4],
    "price": [25, 35, 45, 55, 70, 85, 100],
}
df_model = pd.DataFrame(train_data)

# Train the model
X = df_model[["area", "bedrooms"]]
y = df_model["price"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

# Display model metrics
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

col1, col2 = st.columns(2)
col1.metric("Model MAE (Error)", f"{mae:.2f} Lakhs")
col2.metric("R² Score (Accuracy)", f"{r2:.2f}")

# Interactive Prediction Input for the Live Demo
st.write("### Test Custom Property Price")
user_area = st.number_input("Enter Area (sqft):", value=1400)
user_beds = st.selectbox("Select Bedrooms:", [1, 2, 3, 4, 5], index=2)

if st.button("Predict Price"):
  predicted_price = model.predict([[user_area, user_beds]])[0]
  st.success(f"Estimated Property Price: **₹{predicted_price:.2f} Lakhs**")
    
