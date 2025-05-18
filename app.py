import streamlit as st
import pandas as pd
import joblib

# Load trained model and feature columns
model = joblib.load("genetic_risk_model.pkl")
model_columns = joblib.load("model_features.pkl")

# Genetic diseases categorized with inheritance and symptoms
disease_info = {
    "Autosomal Dominant Disorders": {
        "Huntington’s Disease": ["Autosomal Dominant", ["Involuntary movements", "Cognitive decline", "Mood swings"]],
        "Marfan Syndrome": ["Autosomal Dominant", ["Tall stature", "Long limbs", "Heart defects"]],
        "Achondroplasia": ["Autosomal Dominant", ["Short limbs", "Large head", "Frequent ear infections"]],
        "Familial Hypercholesterolemia": ["Autosomal Dominant", ["High LDL", "Xanthomas", "Early heart disease"]],
        "Neurofibromatosis Type 1 (NF1)": ["Autosomal Dominant", ["Skin spots", "Neurofibromas", "Learning difficulties"]],
        "Polycystic Kidney Disease (Adult Type)": ["Autosomal Dominant", ["High blood pressure", "Kidney cysts", "Flank pain"]],
    },
    "Autosomal Recessive Disorders": {
        "Cystic Fibrosis": ["Autosomal Recessive", ["Cough", "Respiratory infections", "Salty skin"]],
        "Sickle Cell Anemia": ["Autosomal Recessive", ["Anemia", "Pain crises", "Swelling"]],
        "Tay-Sachs Disease": ["Autosomal Recessive", ["Muscle weakness", "Seizures", "Vision loss"]],
        "Phenylketonuria (PKU)": ["Autosomal Recessive", ["Intellectual disability", "Musty odor", "Skin rashes"]],
        "Thalassemia": ["Autosomal Recessive", ["Fatigue", "Pale skin", "Enlarged spleen"]],
        "Gaucher’s Disease": ["Autosomal Recessive", ["Bone pain", "Anemia", "Enlarged liver"]],
    },
    "X-linked Recessive Disorders": {
        "Hemophilia A and B": ["X-linked Recessive", ["Bleeding", "Joint pain", "Bruising"]],
        "Duchenne Muscular Dystrophy": ["X-linked Recessive", ["Muscle weakness", "Gait abnormality", "Enlarged calves"]],
        "Color Blindness (Red-Green)": ["X-linked Recessive", ["Color vision issues", "Difficulty distinguishing red & green"]],
        "Fragile X Syndrome": ["X-linked Recessive", ["Learning disabilities", "Long face", "Hyperactivity"]],
        "G6PD Deficiency": ["X-linked Recessive", ["Fatigue", "Jaundice", "Dark urine"]],
    },
    "Mitochondrial Inheritance": {
        "Leber’s Hereditary Optic Neuropathy (LHON)": ["Mitochondrial", ["Vision loss", "Eye pain", "Central vision issues"]],
        "Mitochondrial Myopathy": ["Mitochondrial", ["Muscle weakness", "Fatigue", "Exercise intolerance"]],
        "MELAS Syndrome": ["Mitochondrial", ["Seizures", "Stroke-like episodes", "Lactic acidosis"]],
    }
}

# UI starts
st.set_page_config(page_title="Genetic Disease Risk Predictor", layout="centered")
st.title("🧬 Genetic Disease Risk Predictor")

# Disease selection
st.subheader("🔍 Select a Genetic Disorder")
category = st.selectbox("Disorder Category", list(disease_info.keys()))
disease = st.selectbox("Specific Disorder", list(disease_info[category].keys()))

# Display info
inheritance_type, symptoms = disease_info[category][disease]
st.info(f"**Inheritance Type:** {inheritance_type}")
st.write("**Common Symptoms:**")
for s in symptoms:
    st.write(f"• {s}")

st.subheader("🧑‍⚕️ Family Medical History")
mother_has = st.selectbox("Does mother have this disorder?", ["Yes", "No"])
father_has = st.selectbox("Does father have this disorder?", ["Yes", "No"])
grandparents = st.multiselect("Select grandparents who had this disorder", ["Maternal Grandmother", "Maternal Grandfather", "Paternal Grandmother", "Paternal Grandfather"])

st.subheader("👶 Child Information")
gender = st.selectbox("Gender of child", ["Male", "Female", "Unknown"])
birth_defect = st.selectbox("Observed any birth defects?", ["No", "Yes", "Singular", "Multiple"])
folic = st.selectbox("Folic acid taken during conception?", ["Yes", "No", "Not Sure"])

# Construct input DataFrame
input_data = {
    "Mother's age": [30],
    "Father's age": [32],
    'Birth defects': [birth_defect],
    'Gender': [gender],
    "Genes in mother's side": ["Yes" if "Maternal Grandmother" in grandparents or "Maternal Grandfather" in grandparents else "No"],
    'Inherited from father': ["Yes" if "Paternal Grandfather" in grandparents else "No"],
    'Maternal gene': [mother_has],
    'Paternal gene': [father_has],
    'Folic acid details (peri-conceptional)': [folic],
    'H/O serious maternal illness': [st.selectbox("History of serious maternal illness?", ["Yes", "No"])],
    'H/O radiation exposure (x-ray)': [st.selectbox("Radiation exposure during pregnancy?", ["Yes", "No"])],
    'H/O substance abuse': [st.selectbox("Substance abuse during pregnancy?", ["Yes", "No"])],
    'Assisted conception IVF/ART': [st.selectbox("Was IVF/ART used?", ["Yes", "No"])],
    'History of anomalies in previous pregnancies': [st.selectbox("History of anomalies in past pregnancies?", ["Yes", "No"])],
    'No. of previous abortion': [st.slider("Number of previous abortions", 0, 5, 0)]
}

input_df = pd.DataFrame(input_data)

# Encode and align
input_encoded = pd.get_dummies(input_df)
input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)

# Predict button
if st.button("🔬 Predict Risk"):
    prediction = model.predict(input_encoded)[0]
    prediction_proba = model.predict_proba(input_encoded)[0]
    confidence = max(prediction_proba) * 100
    st.success(f"🧠 Predicted Risk Level for {disease}: **{prediction}**")
    st.info(f"📊 Risk Confidence: **{confidence:.2f}%**")

    st.markdown("### 🩺 Recommended Steps:")
    if prediction == "High":
        st.warning("👉 Consult a genetic counselor immediately. Early screening and prenatal tests advised.")
    elif prediction == "Moderate":
        st.info("⚠️ Genetic consultation recommended. Maintain medical surveillance.")
    else:
        st.success("✅ Low risk. Maintain regular check-ups and a healthy lifestyle.")
