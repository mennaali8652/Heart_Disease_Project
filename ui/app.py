# Streamlit Web UI Development
import streamlit as st
import joblib
import json
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'final_pipeline.pkl')
model = joblib.load(MODEL_PATH)

# loading feature names
file_path = os.path.join(BASE_DIR, '..', "models", "feature_names.json")
with open(file_path) as f:
    feature_names = json.load(f)

feature_descriptions = {
    "fbs": ("Fasting Blood Sugar", "1 = >120 mg/dl, 0 = otherwise"),
    "thal": ("Thalassemia", "1 = normal, 2 = fixed defect, 3 = reversible defect"),
    "oldpeak": ("ST Depression", "Relative to rest"),
    "sex": ("Sex", "0 = female, 1 = male"),
    "slope": ("Slope of ST Segment", "0 = upsloping, 1 = flat, 2 = downsloping"),
    "ca": ("Major Vessels Colored", "0–3 vessels seen via fluoroscopy"),
    "thalach": ("Max Heart Rate Achieved", "Measured during exercise"),
    "restecg": ("Resting ECG Results", "0 = normal, 1 = ST-T abnormality, 2 = LV hypertrophy"),
    "cp": ("Chest Pain Type", "0 = typical angina, 1 = atypical angina, 2 = non-anginal pain, 3 = asymptomatic")
}

st.set_page_config(page_title="Heart Disease Classifier", page_icon="🫀", layout="centered")
st.title("Heart Disease Risk Classifier")
st.markdown("""
This tool predicts the risk category of heart disease based on selected health indicators.

Please enter the required values below. All inputs are numeric and based on standard medical measurements.
""")

# user input
st.subheader("📝 Patient Health Information")
user_input = []
cols = st.columns(2)

for i, feature in enumerate(feature_names):
    label, help_text = feature_descriptions.get(feature, (feature, ""))
    with cols[i % 2]:
        val = st.number_input(label, value=0.0, help=help_text)
        user_input.append(val)

# prediction
risk_labels = {
    0: "No disease",
    1: "Low risk",
    2: "Moderate risk",
    3: "High risk",
    4: "Very high risk"
}

if st.button("Predict 🔍"):
    input_array = np.array(user_input).reshape(1, -1)
    prediction = model.predict(input_array)[0]
    label = risk_labels.get(prediction, "Unknown")
    st.success(f"🧠 Predicted Category: {prediction} — {label}")

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_array)[0]
        st.subheader("📊 Prediction Probabilities:")
        prob_df = {f"Category {i}": round(p, 2) for i, p in enumerate(probs)}
        st.bar_chart(prob_df)
