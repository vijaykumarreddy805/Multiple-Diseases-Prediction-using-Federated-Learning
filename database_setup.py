# ============================================
# PATIENT RECORDS DATABASE SETUP
# Multi-Disease Prediction System
# ============================================

import mysql.connector
from mysql.connector import Error
import pandas as pd
import hashlib

def create_database_connection():
    """Create database connection"""
    try:
        # Update these credentials based on your MySQL setup
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            autocommit=True
        )
        print("✅ MySQL Connection Successful")
        return connection
    except Error as e:
        print(f"❌ Connection Error: {e}")
        return None

def create_database_and_tables():
    """Create database and tables for patient records"""
    connection = create_database_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS patient_records")
        cursor.execute("USE patient_records")
        print("✅ Database 'patient_records' created/selected")
        
        # Create patients table
        create_patients_table = """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            age INT,
            gender ENUM('Male', 'Female', 'Other'),
            date_of_birth DATE,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_patients_table)
        print("✅ Patients table created")
        
        # Create diabetes_predictions table
        create_diabetes_table = """
        CREATE TABLE IF NOT EXISTS diabetes_predictions (
            prediction_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            pregnancies INT,
            glucose DECIMAL(5,2),
            blood_pressure DECIMAL(5,2),
            skin_thickness DECIMAL(5,2),
            insulin DECIMAL(6,2),
            bmi DECIMAL(4,2),
            diabetes_pedigree_function DECIMAL(5,4),
            age INT,
            prediction_probability DECIMAL(5,4),
            prediction_result ENUM('Positive', 'Negative'),
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
        """
        cursor.execute(create_diabetes_table)
        print("✅ Diabetes predictions table created")
        
        # Create heart_predictions table
        create_heart_table = """
        CREATE TABLE IF NOT EXISTS heart_predictions (
            prediction_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            age INT,
            sex INT,
            chest_pain_type INT,
            resting_bp DECIMAL(5,2),
            cholesterol DECIMAL(5,2),
            fasting_bs INT,
            resting_ecg INT,
            max_heart_rate INT,
            exercise_angina INT,
            oldpeak DECIMAL(4,2),
            st_slope INT,
            ca INT,
            thal INT,
            prediction_probability DECIMAL(5,4),
            prediction_result ENUM('Positive', 'Negative'),
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
        """
        cursor.execute(create_heart_table)
        print("✅ Heart predictions table created")
        
        # Create liver_predictions table
        create_liver_table = """
        CREATE TABLE IF NOT EXISTS liver_predictions (
            prediction_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            age INT,
            gender INT,
            total_bilirubin DECIMAL(5,2),
            direct_bilirubin DECIMAL(5,2),
            alkaline_phosphatase INT,
            alamine_aminotransferase INT,
            aspartate_aminotransferase INT,
            total_proteins DECIMAL(5,2),
            albumin DECIMAL(4,2),
            albumin_globulin_ratio DECIMAL(4,2),
            prediction_probability DECIMAL(5,4),
            prediction_result ENUM('Positive', 'Negative'),
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
        """
        cursor.execute(create_liver_table)
        print("✅ Liver predictions table created")
        
        # Create kidney_predictions table
        create_kidney_table = """
        CREATE TABLE IF NOT EXISTS kidney_predictions (
            prediction_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            id INT,
            age INT,
            blood_pressure DECIMAL(5,2),
            specific_gravity DECIMAL(3,2),
            albumin INT,
            sugar INT,
            red_blood_cells INT,
            pus_cell INT,
            pus_cell_clumps INT,
            bacteria INT,
            blood_glucose_random DECIMAL(6,2),
            blood_urea DECIMAL(6,2),
            serum_creatinine DECIMAL(5,2),
            sodium DECIMAL(5,2),
            potassium DECIMAL(4,2),
            hemoglobin DECIMAL(4,2),
            packed_cell_volume DECIMAL(4,2),
            white_blood_cell_count DECIMAL(8,2),
            red_blood_cell_count DECIMAL(8,2),
            hypertension INT,
            diabetes_mellitus INT,
            coronary_artery_disease INT,
            appetite INT,
            peda_edema INT,
            anemia INT,
            prediction_probability DECIMAL(5,4),
            prediction_result ENUM('Positive', 'Negative'),
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
        """
        cursor.execute(create_kidney_table)
        print("✅ Kidney predictions table created")
        
        # Create sample patient data
        insert_sample_patient = """
        INSERT IGNORE INTO patients (name, email, phone, age, gender) 
        VALUES ('John Doe', 'john.doe@email.com', '123-456-7890', 35, 'Male')
        """
        cursor.execute(insert_sample_patient)
        print("✅ Sample patient data inserted")
        
        print("\n🎉 Database setup completed successfully!")
        print("📊 Database: patient_records")
        print("📋 Tables created: patients, diabetes_predictions, heart_predictions, liver_predictions, kidney_predictions")
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        cursor.close()
        connection.close()

def show_connection_info():
    """Display MySQL Workbench connection information"""
    print("\n🔗 MySQL Workbench Connection Details:")
    print("=" * 50)
    print("📝 Connection Name: Patient Records DB")
    print("🏠 Hostname: localhost")
    print("🚪 Port: 3306")
    print("👤 Username: root")
    print("🔑 Password: Vijay@123")
    print("🗄️ Default Schema: patient_records")
    print("=" * 50)
    print("\n📋 Steps to connect in MySQL Workbench:")
    print("1. Open MySQL Workbench")
    print("2. Click '+' to create new connection")
    print("3. Enter the details above")
    print("4. Test Connection")
    print("5. Click OK to save and connect")

if __name__ == "__main__":
    print("🏥 Setting up Patient Records Database...")
    create_database_and_tables()
    show_connection_info()
