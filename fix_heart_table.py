# ============================================
# FIX HEART PREDICTIONS TABLE
# ============================================

import mysql.connector
from mysql.connector import Error

def fix_heart_table():
    """Fix heart predictions table with missing columns"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Vijay@123',
            database='patient_records',
            autocommit=True
        )
        cursor = connection.cursor()
        
        # Add missing columns if they don't exist
        try:
            cursor.execute("ALTER TABLE heart_predictions ADD COLUMN ca INT")
            print("✅ Added 'ca' column")
        except Error:
            print("⚠️ 'ca' column already exists")
            
        try:
            cursor.execute("ALTER TABLE heart_predictions ADD COLUMN thal INT")
            print("✅ Added 'thal' column")
        except Error:
            print("⚠️ 'thal' column already exists")
        
        # Show table structure
        cursor.execute("DESCRIBE heart_predictions")
        columns = cursor.fetchall()
        
        print("\n📊 Heart Predictions Table Structure:")
        for column in columns:
            print(f"  - {column[0]} ({column[1]})")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Heart table fixed successfully!")
        
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_heart_table()
