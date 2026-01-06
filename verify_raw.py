import sqlite3
import os

db_path = "enterprise_ai.db"

if not os.path.exists(db_path):
    print("Database file does not exist.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT email, is_active FROM users WHERE email='admin@enterprise.com'")
    result = cursor.fetchone()
    if result:
        print(f"Superuser Found: {result[0]}, Active: {result[1]}")
    else:
        print("Superuser NOT found.")
        
    cursor.execute("SELECT name FROM roles")
    roles = cursor.fetchall()
    print(f"Roles Found: {[r[0] for r in roles]}")

except Exception as e:
    print(f"Error querying DB: {e}")

conn.close()
