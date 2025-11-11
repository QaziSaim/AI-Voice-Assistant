import sqlite3, os

db_path = r"E:\MLOPOS\riverwood_project\memory_db\riverwood_memory.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
conn.close()

print("✅ Empty database created at:", db_path)
