import streamlit as st
import numpy as np
import pandas as pd
import joblib
import mysql.connector
from mysql.connector import Error
from datetime import datetime

st.set_page_config(page_title="Multi Disease Prediction", layout="wide")

st.title("🩺 Multi-Disease Prediction System")
st.write("Diabetes | Heart | Liver | Kidney")

st.divider()

# Load models and data
@st.cache_resource
def load_models():
    # Diabetes
    model_d = joblib.load("models/diabetes_nn.pkl")
    xgb_d = joblib.load("models/diabetes_xgb.pkl")
    scaler_d = joblib.load("models/diabetes_scaler.pkl")
    
    # Heart
    model_h = joblib.load("models/heart_nn.pkl")
    xgb_h = joblib.load("models/heart_xgb.pkl")
    scaler_h = joblib.load("models/heart_scaler.pkl")
    heart = pd.read_csv("heart.csv")
    X_h = heart.drop("target", axis=1)
    
    # Liver
    model_l = joblib.load("models/liver_nn.pkl")
    xgb_l = joblib.load("models/liver_xgb.pkl")
    scaler_l = joblib.load("models/liver_scaler.pkl")
    liver = pd.read_csv("liver.csv")
    if "Gender" in liver.columns:
        liver["Gender"] = pd.to_numeric(liver["Gender"], errors="coerce")
    liver = liver.fillna(liver.median())
    X_l = liver.drop("Dataset", axis=1)
    
    # Kidney
    model_k = joblib.load("models/kidney_nn.pkl")
    xgb_k = joblib.load("models/kidney_xgb.pkl")
    scaler_k = joblib.load("models/kidney_scaler.pkl")
    kidney = pd.read_csv("kidney_disease.csv")
    kidney.replace({
        "yes": 1, "no": 0,
        "present": 1, "notpresent": 0,
        "abnormal": 1, "normal": 0,
        "poor": 1, "good": 0,
        "ckd": 1, "notckd": 0
    }, inplace=True)
    kidney = kidney.apply(pd.to_numeric, errors="coerce")
    kidney = kidney.fillna(kidney.median())
    X_k = kidney.drop("classification", axis=1)
    
    return {
        'model_d': model_d, 'xgb_d': xgb_d, 'scaler_d': scaler_d,
        'model_h': model_h, 'xgb_h': xgb_h, 'scaler_h': scaler_h, 'X_h': X_h,
        'model_l': model_l, 'xgb_l': xgb_l, 'scaler_l': scaler_l, 'X_l': X_l,
        'model_k': model_k, 'xgb_k': xgb_k, 'scaler_k': scaler_k, 'X_k': X_k
    }

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='patient_records',
            autocommit=True
        )
        return connection
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

def save_diabetes_prediction(values, probability, result):
    """Save diabetes prediction to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # First save patient
            insert_patient = """
            INSERT INTO patients (name, email, age, gender)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_patient, ('Anonymous Patient', f'patient{int(values[7])}@email.com', int(values[7]), 'Other'))
            
            # Get patient_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            patient_id = cursor.fetchone()[0]
            
            # Convert numpy types to Python native types
            clean_values = [float(v) for v in values]
            clean_prob = float(probability)
            
            # Save prediction
            insert_prediction = """
            INSERT INTO diabetes_predictions 
            (patient_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, 
             diabetes_pedigree_function, age, prediction_probability, prediction_result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_prediction, (
                int(patient_id), clean_values[0], clean_values[1], clean_values[2], 
                clean_values[3], clean_values[4], clean_values[5], clean_values[6], 
                int(clean_values[7]), clean_prob, result
            ))
            
            cursor.close()
            st.success(f"✅ Prediction saved to database! (Patient ID: {patient_id})")
            
        except Error as e:
            st.error(f"Error saving to database: {e}")
        finally:
            connection.close()

def save_heart_prediction(values, probability, result):
    """Save heart prediction to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # First save patient
            insert_patient = """
            INSERT INTO patients (name, email, age, gender)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_patient, ('Anonymous Patient', f'heart{int(values[0])}@email.com', int(values[0]), 'Male' if values[1] == 1 else 'Female'))
            
            # Get patient_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            patient_id = cursor.fetchone()[0]
            
            # Convert numpy types to Python native types
            clean_values = [float(v) for v in values]
            clean_prob = float(probability)
            
            # Save prediction
            insert_prediction = """
            INSERT INTO heart_predictions 
            (patient_id, age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, 
             resting_ecg, max_heart_rate, exercise_angina, oldpeak, st_slope, ca, thal,
             prediction_probability, prediction_result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_prediction, (
                int(patient_id), clean_values[0], clean_values[1], clean_values[2], 
                clean_values[3], clean_values[4], clean_values[5], clean_values[6], 
                clean_values[7], clean_values[8], clean_values[9], clean_values[10], 
                clean_values[11], clean_values[12], clean_prob, result
            ))
            
            cursor.close()
            st.success(f"✅ Heart prediction saved to database! (Patient ID: {patient_id})")
            
        except Error as e:
            st.error(f"Error saving to database: {e}")
        finally:
            connection.close()

def save_liver_prediction(values, probability, result):
    """Save liver prediction to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # First save patient
            insert_patient = """
            INSERT INTO patients (name, email, age, gender)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_patient, ('Anonymous Patient', f'liver{int(values[0])}@email.com', int(values[0]), 'Male' if values[1] == 1 else 'Female'))
            
            # Get patient_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            patient_id = cursor.fetchone()[0]
            
            # Convert numpy types to Python native types
            clean_values = [float(v) for v in values]
            clean_prob = float(probability)
            
            # Save prediction
            insert_prediction = """
            INSERT INTO liver_predictions 
            (patient_id, age, gender, total_bilirubin, direct_bilirubin, alkaline_phosphatase, 
             alamine_aminotransferase, aspartate_aminotransferase, total_proteins, albumin, 
             albumin_globulin_ratio, prediction_probability, prediction_result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_prediction, (
                int(patient_id), clean_values[0], clean_values[1], clean_values[2], 
                clean_values[3], clean_values[4], clean_values[5], clean_values[6], 
                clean_values[7], clean_values[8], clean_values[9], clean_prob, result
            ))
            
            cursor.close()
            st.success(f"✅ Liver prediction saved to database! (Patient ID: {patient_id})")
            
        except Error as e:
            st.error(f"Error saving to database: {e}")
        finally:
            connection.close()

def save_kidney_prediction(values, probability, result):
    """Save kidney prediction to database"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # First save patient
            insert_patient = """
            INSERT INTO patients (name, email, age, gender)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_patient, ('Anonymous Patient', f'kidney{int(values[0])}@email.com', int(values[0]), 'Other'))
            
            # Get patient_id
            cursor.execute("SELECT LAST_INSERT_ID()")
            patient_id = cursor.fetchone()[0]
            
            # Convert numpy types to Python native types
            clean_values = [float(v) for v in values]
            clean_prob = float(probability)
            
            # Save prediction
            insert_prediction = """
            INSERT INTO kidney_predictions 
            (patient_id, id, age, blood_pressure, specific_gravity, albumin, sugar, red_blood_cells, 
             pus_cell, pus_cell_clumps, bacteria, blood_glucose_random, blood_urea, serum_creatinine, 
             sodium, potassium, hemoglobin, packed_cell_volume, white_blood_cell_count, red_blood_cell_count, 
             hypertension, diabetes_mellitus, coronary_artery_disease, appetite, peda_edema, anemia, 
             prediction_probability, prediction_result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_prediction, (
                int(patient_id), clean_values[0], clean_values[1], clean_values[2], clean_values[3], clean_values[4], 
                clean_values[5], clean_values[6], clean_values[7], clean_values[8], clean_values[9], 
                clean_values[10], clean_values[11], clean_values[12], clean_values[13], clean_values[14], 
                clean_values[15], clean_values[16], clean_values[17], clean_values[18], clean_values[19], 
                clean_values[20], clean_values[21], clean_values[22], clean_values[23], clean_values[24], clean_prob, result
            ))
            
            cursor.close()
            st.success(f"✅ Kidney prediction saved to database! (Patient ID: {patient_id})")
            
        except Error as e:
            st.error(f"Error saving to database: {e}")
        finally:
            connection.close()

models = load_models()

def get_user_inputs(columns, dataset):
    values = []
    for col in columns:
        low = float(dataset[col].min())
        high = float(dataset[col].max())
        val = st.number_input(
            f"{col} ({low:.2f} - {high:.2f})",
            min_value=low,
            max_value=high,
            value=(low + high) / 2
        )
        values.append(val)
    return values


def show_result(disease, positive, values=None):
    if not positive:
        st.success(f"No {disease} detected")
    else:
        st.error(f"{disease} detected")
        if disease == "Diabetes":
            show_diabetes_precautions(values)
        elif disease == "Heart Disease":
            show_heart_precautions(values)
        elif disease == "Liver Disease":
            show_liver_precautions(values)
        elif disease == "Kidney Disease":
            show_kidney_precautions(values)

def show_diabetes_precautions(values):
    if values is None:
        return
    
    glucose, bp, bmi, insulin = values[1], values[2], values[5], values[4]
    
    st.subheader("🚨 Diabetes Analysis & Precautions")
    
    # Critical Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Your Values Analysis:**")
        if glucose > 126:
            st.error(f"🔴 Glucose: {glucose} mg/dL (CRITICAL - Normal: 70-100)")
        elif glucose > 100:
            st.warning(f"🟡 Glucose: {glucose} mg/dL (PREDIABETES - Normal: 70-100)")
        else:
            st.success(f"🟢 Glucose: {glucose} mg/dL (NORMAL)")
            
        if bp > 140:
            st.error(f"🔴 BP: {bp} mmHg (HIGH - Normal: <120)")
        elif bp > 120:
            st.warning(f"🟡 BP: {bp} mmHl (ELEVATED - Normal: <120)")
        else:
            st.success(f"🟢 BP: {bp} mmHg (NORMAL)")
    
    with col2:
        st.write("**📋 Immediate Actions:**")
        if glucose > 200:
            st.error("🚨 SEEK EMERGENCY CARE")
            st.error("🚨 Glucose >200 is DANGEROUS")
        elif glucose > 126:
            st.warning("⚠️ Consult Doctor IMMEDIATELY")
            st.warning("⚠️ Start Diabetes Treatment")
        
        if bmi < 18.5:
            st.warning("⚠️ Underweight - Nutrition needed")
        elif bmi > 30:
            st.warning("⚠️ Obesity - Weight loss required")
    
    st.divider()
    
    # Precautions by category
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🍎 Diet Control")
        st.write("• Eliminate refined sugars")
        st.write("• Low glycemic foods")
        st.write("• High fiber vegetables")
        st.write("• Small frequent meals")
        st.write("• No sugary drinks")
    
    with col2:
        st.subheader("🏃 Exercise Plan")
        st.write("• 30 min daily walk")
        st.write("• Monitor glucose during")
        st.write("• Start slow, progress")
        st.write("• Strength training")
        st.write("• Yoga/meditation")
    
    with col3:
        st.subheader("💊 Medical Care")
        st.write("• Check glucose 4x daily")
        st.write("• Take medications on time")
        st.write("• Regular doctor visits")
        st.write("• Foot care daily")
        st.write("• Eye exams annually")

def show_heart_precautions(values):
    st.subheader("❤️ Heart Disease Precautions")
    st.write("• Reduce salt intake")
    st.write("• Avoid smoking completely")
    st.write("• Daily walking exercise")
    st.write("• Monitor cholesterol")
    st.write("• Manage stress levels")

def show_liver_precautions(values):
    st.subheader("🧬 Liver Disease Precautions")
    st.write("• Avoid alcohol completely")
    st.write("• Drink more water")
    st.write("• Eat fresh fruits")
    st.write("• Avoid processed foods")
    st.write("• Regular liver function tests")

def show_kidney_precautions(values):
    st.subheader("🩸 Kidney Disease Precautions")
    st.write("• Reduce salt intake")
    st.write("• Avoid painkillers")
    st.write("• Stay hydrated")
    st.write("• Control blood pressure")
    st.write("• Regular kidney function tests")


st.header("Enter Patient Details")

with st.expander("🧪 Diabetes Inputs"):
    st.write("**📊 Dataset-Based Ranges Shown in Parentheses**")
    
    preg = st.number_input("Pregnancies (0-17)", 0, 20)
    glucose = st.number_input("Glucose (0-199 mg/dL)", 0, 300)
    bp = st.number_input("Blood Pressure (0-122 mmHg)", 0, 200)
    skin = st.number_input("Skin Thickness (0-99 mm)", 0, 100)
    insulin = st.number_input("Insulin (0-846 μU/mL)", 0, 900)
    bmi = st.number_input("BMI (0.0-67.1 kg/m²)", 0.0, 70.0)
    dpf = st.number_input("Diabetes Pedigree Function (0.078-2.420)", 0.0, 3.0)
    age = st.number_input("Age (21-81 years)", 0, 120)
    
    # Real-time analysis
    diabetes_values = [preg, glucose, bp, skin, insulin, bmi, dpf, age]
    
    st.write("**🔍 Real-time Analysis:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if glucose > 126:
            st.error("🔴 HIGH Glucose")
        elif glucose > 100:
            st.warning("🟡 Prediabetes")
        else:
            st.success("🟢 Normal Glucose")
    
    with col2:
        if bp > 140:
            st.error("🔴 HIGH BP")
        elif bp > 120:
            st.warning("🟡 Elevated BP")
        else:
            st.success("🟢 Normal BP")
    
    with col3:
        if bmi < 18.5:
            st.warning("🟡 Underweight")
        elif bmi > 30:
            st.error("🔴 Obese")
        else:
            st.success("🟢 Normal BMI")
    
    with col4:
        if age > 45:
            st.warning("🟡 Age Risk")
        else:
            st.success("🟢 Lower Risk")

    if st.button("Predict Diabetes"):
        data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
        data_scaled = models['scaler_d'].transform(data)

        prob = (models['model_d'].predict(data_scaled)[0][0] +
                models['xgb_d'].predict_proba(data_scaled)[0][1]) / 2
        
        st.divider()
        st.subheader("🎯 Prediction Results")
        st.write(f"**Diabetes Probability: {prob:.1%}**")
        
        result = "Positive" if prob > 0.5 else "Negative"
        
        if prob > 0.5:
            show_result("Diabetes", True, diabetes_values)
        else:
            show_result("Diabetes", False, diabetes_values)
        
        # Save to database
        save_diabetes_prediction(diabetes_values, prob, result)


# Heart Disease Prediction Section
with st.expander("❤️ Heart Disease Inputs"):
    st.write("**📊 Dataset-Based Ranges Shown in Parentheses**")
    
    col1, col2 = st.columns(2)
    with col1:
        age_heart = st.number_input("Age (29-77 years)", 29, 77)
        sex_heart = st.selectbox("Sex", ['Male', 'Female'])
        chest_pain = st.selectbox("Chest Pain Type (0-3)", [0, 1, 2, 3])
        resting_bp = st.number_input("Resting BP (94-200 mmHg)", 94, 200)
        cholesterol = st.number_input("Cholesterol (126-564 mg/dL)", 126, 564)
        
    with col2:
        fasting_bs = st.selectbox("Fasting Blood Sugar (0-1)", [0, 1])
        resting_ecg = st.selectbox("Resting ECG (0-2)", [0, 1, 2])
        max_hr = st.number_input("Max Heart Rate (71-202)", 71, 202)
        exercise_angina = st.selectbox("Exercise Angina (0-1)", [0, 1])
        oldpeak = st.number_input("Oldpeak (0.0-6.2)", 0.0, 6.2)
        
    st_slope = st.selectbox("ST Slope (0-2)", [0, 1, 2])
    ca = st.selectbox("CA (0-4)", [0, 1, 2, 3, 4])
    thal = st.selectbox("Thal (0-3)", [0, 1, 2, 3])
    
    # Map sex to numeric
    sex_heart_mapped = 1 if sex_heart == 'Male' else 0
    
    heart_values = [age_heart, sex_heart_mapped, chest_pain, resting_bp, cholesterol, 
                  fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope, ca, thal]
    
    st.write("**🔍 Real-time Analysis:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if age_heart > 55:
            st.warning("🟡 Age Risk Factor")
        else:
            st.success("🟢 Lower Age Risk")
            
    with col2:
        if cholesterol > 200:
            st.error("🔴 High Cholesterol")
        else:
            st.success("🟢 Normal Cholesterol")
            
    with col3:
        if resting_bp > 140:
            st.error("🔴 High BP")
        else:
            st.success("🟢 Normal BP")

    if st.button("Predict Heart Disease"):
        data = np.array([heart_values])
        data_scaled = models['scaler_h'].transform(data)
        
        prob = (models['model_h'].predict(data_scaled)[0][0] + 
                models['xgb_h'].predict_proba(data_scaled)[0][1]) / 2
        
        st.divider()
        st.subheader("🎯 Heart Disease Prediction Results")
        st.write(f"**Heart Disease Probability: {prob:.1%}**")
        
        result = "Positive" if prob > 0.5 else "Negative"
        
        if prob > 0.5:
            show_result("Heart Disease", True, heart_values)
        else:
            show_result("Heart Disease", False, heart_values)
        
        save_heart_prediction(heart_values, prob, result)

# Liver Disease Prediction Section  
with st.expander("🧬 Liver Disease Inputs"):
    st.write("**📊 Dataset-Based Ranges Shown in Parentheses**")
    
    col1, col2 = st.columns(2)
    with col1:
        age_liver = st.number_input("Age (4-90 years)", 4, 90)
        gender_liver = st.selectbox("Gender", ['Male', 'Female'])
        total_bilirubin = st.number_input("Total Bilirubin (0.4-75.0)", 0.4, 75.0)
        direct_bilirubin = st.number_input("Direct Bilirubin (0.1-19.7)", 0.1, 19.7)
        alkaline_phosphotase = st.number_input("Alkaline Phosphotase (63-2110)", 63, 2110)
        
    with col2:
        alamine_aminotransferase = st.number_input("Alamine Aminotransferase (10-2000)", 10, 2000)
        aspartate_aminotransferase = st.number_input("Aspartate Aminotransferase (10-4929)", 10, 4929)
        total_proteins = st.number_input("Total Proteins (2.7-9.6)", 2.7, 9.6)
        albumin = st.number_input("Albumin (0.9-5.5)", 0.9, 5.5)
        albumin_globulin_ratio = st.number_input("Albumin/Globulin Ratio (0.3-2.8)", 0.3, 2.8)
    
    # Map gender to numeric (Male=1, Female=0)
    gender_liver_mapped = 1 if gender_liver == 'Male' else 0
    
    liver_values = [age_liver, gender_liver_mapped, total_bilirubin, direct_bilirubin, 
                  alkaline_phosphotase, alamine_aminotransferase, aspartate_aminotransferase,
                  total_proteins, albumin, albumin_globulin_ratio]
    
    st.write("**🔍 Real-time Analysis:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if age_liver > 50:
            st.warning("🟡 Age Risk Factor")
        else:
            st.success("🟢 Lower Age Risk")
            
    with col2:
        if total_bilirubin > 1.2:
            st.error("🔴 High Bilirubin")
        else:
            st.success("🟢 Normal Bilirubin")
            
    with col3:
        if albumin < 3.5:
            st.warning("🟡 Low Albumin")
        else:
            st.success("🟢 Normal Albumin")

    if st.button("Predict Liver Disease"):
        data = np.array([liver_values])
        data_scaled = models['scaler_l'].transform(data)
        
        prob = (models['model_l'].predict(data_scaled)[0][0] + 
                models['xgb_l'].predict_proba(data_scaled)[0][1]) / 2
        
        st.divider()
        st.subheader("🎯 Liver Disease Prediction Results")
        st.write(f"**Liver Disease Probability: {prob:.1%}**")
        
        result = "Positive" if prob > 0.5 else "Negative"
        
        if prob > 0.5:
            show_result("Liver Disease", True, liver_values)
        else:
            show_result("Liver Disease", False, liver_values)
        
        save_liver_prediction(liver_values, prob, result)

# Kidney Disease Prediction Section
with st.expander("🩸 Kidney Disease Inputs"):
    st.write("**📊 Dataset-Based Ranges Shown in Parentheses**")
    
    col1, col2 = st.columns(2)
    with col1:
        age_kidney = st.number_input("Age (2-90 years)", 2, 90)
        blood_pressure_kidney = st.number_input("Blood Pressure (50-180 mmHg)", 50, 180)
        specific_gravity = st.number_input("Specific Gravity (1.005-1.025)", 1.005, 1.025)
        albumin_kidney = st.selectbox("Albumin (0-5)", [0, 1, 2, 3, 4, 5])
        sugar_kidney = st.selectbox("Sugar (0-5)", [0, 1, 2, 3, 4, 5])
        red_blood_cells = st.selectbox("Red Blood Cells (0-1)", [0, 1])
        
    with col2:
        pus_cell = st.selectbox("Pus Cell (0-1)", [0, 1])
        pus_cell_clumps = st.selectbox("Pus Cell Clumps (0-1)", [0, 1])
        bacteria = st.selectbox("Bacteria (0-1)", [0, 1])
        blood_glucose_random = st.number_input("Blood Glucose Random (22-490)", 22, 490)
        blood_urea = st.number_input("Blood Urea (1.1-291)", 1.1, 291.0)
        serum_creatinine = st.number_input("Serum Creatinine (0.4-76.0)", 0.4, 76.0)
        
    # Additional inputs in third column
    col1, col2, col3 = st.columns(3)
    with col1:
        sodium = st.number_input("Sodium (111-155)", 111, 155)
        potassium = st.number_input("Potassium (2.5-7.8)", 2.5, 7.8)
    with col2:
        hemoglobin = st.number_input("Hemoglobin (3.1-17.8)", 3.1, 17.8)
        packed_cell_volume = st.number_input("Packed Cell Volume (9-53)", 9, 53)
    with col3:
        white_blood_cell_count = st.number_input("White Blood Cell Count (2200-26400)", 2200, 26400)
        red_blood_cell_count = st.number_input("Red Blood Cell Count (2.03-8.01)", 2.03, 8.01)
    
    # Additional medical indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        patient_id_kidney = st.number_input("Patient ID (0-400)", 0, 400)
        hypertension = st.selectbox("Hypertension (0-1)", [0, 1])
        diabetes_mellitus = st.selectbox("Diabetes Mellitus (0-1)", [0, 1])
    with col2:
        coronary_artery_disease = st.selectbox("Coronary Artery Disease (0-1)", [0, 1])
        appetite = st.selectbox("Appetite (0-1)", [0, 1])
    with col3:
        peda_edema = st.selectbox("Pedal Edema (0-1)", [0, 1])
        anemia = st.selectbox("Anemia (0-1)", [0, 1])
    
    kidney_values = [patient_id_kidney, age_kidney, blood_pressure_kidney, specific_gravity, albumin_kidney, sugar_kidney, 
                   red_blood_cells, pus_cell, pus_cell_clumps, bacteria, blood_glucose_random,
                   blood_urea, serum_creatinine, sodium, potassium, hemoglobin, 
                   packed_cell_volume, white_blood_cell_count, red_blood_cell_count,
                   hypertension, diabetes_mellitus, coronary_artery_disease, appetite, peda_edema, anemia]
    
    st.write("**🔍 Real-time Analysis:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if age_kidney > 60:
            st.warning("🟡 Age Risk Factor")
        else:
            st.success("🟢 Lower Age Risk")
            
    with col2:
        if blood_pressure_kidney > 140:
            st.error("🔴 High BP")
        else:
            st.success("🟢 Normal BP")
            
    with col3:
        if serum_creatinine > 1.3:
            st.error("🔴 High Creatinine")
        else:
            st.success("🟢 Normal Creatinine")

    if st.button("Predict Kidney Disease"):
        data = np.array([kidney_values])
        data_scaled = models['scaler_k'].transform(data)
        
        prob = (models['model_k'].predict(data_scaled)[0][0] + 
                models['xgb_k'].predict_proba(data_scaled)[0][1]) / 2
        
        st.divider()
        st.subheader("🎯 Kidney Disease Prediction Results")
        st.write(f"**Kidney Disease Probability: {prob:.1%}**")
        
        result = "Positive" if prob > 0.5 else "Negative"
        
        if prob > 0.5:
            show_result("Kidney Disease", True, kidney_values)
        else:
            show_result("Kidney Disease", False, kidney_values)
        
        save_kidney_prediction(kidney_values, prob, result)


st.divider()

st.subheader("🏥 Multi-Disease Prediction System")
st.write("Each disease section has its own prediction button. Enter data and click the respective prediction button.")

# Database Statistics
connection = get_db_connection()
if connection:
    try:
        cursor = connection.cursor()
        
        # Get prediction counts
        cursor.execute("SELECT COUNT(*) FROM diabetes_predictions")
        diabetes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM heart_predictions")
        heart_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM liver_predictions")
        liver_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM kidney_predictions")
        kidney_count = cursor.fetchone()[0]
        
        cursor.close()
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🧪 Diabetes Predictions", diabetes_count)
        with col2:
            st.metric("❤️ Heart Predictions", heart_count)
        with col3:
            st.metric("🧬 Liver Predictions", liver_count)
        with col4:
            st.metric("🩸 Kidney Predictions", kidney_count)
            
    except Error as e:
        st.error(f"Error getting statistics: {e}")
    finally:
        if connection:
            connection.close()
