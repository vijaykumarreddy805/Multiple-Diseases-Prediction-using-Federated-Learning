# ============================================
# FIX KIDNEY PREDICTIONS TABLE
# ============================================

import mysql.connector
from mysql.connector import Error

def fix_kidney_table():
    """Fix kidney predictions table with missing id column"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='patient_records',
            autocommit=True
        )
        cursor = connection.cursor()
        
        # Add missing id column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE kidney_predictions ADD COLUMN id INT AFTER patient_id")
            print("✅ Added 'id' column to kidney_predictions")
        except Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ 'id' column already exists in kidney_predictions")
            else:
                print(f"⚠️ Error adding id column: {e}")
        
        # Show table structure
        cursor.execute("DESCRIBE kidney_predictions")
        columns = cursor.fetchall()
        
        print("\n📊 Kidney Predictions Table Structure:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Kidney table fixed successfully!")
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_kidney_table()
