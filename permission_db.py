import os
db_path = os.path.join(os.getcwd(), "memory_db", "riverwood_memory.db")
print("Database Path:", db_path)
print("Exists:", os.path.exists(db_path))
print("Writable:", os.access(db_path, os.W_OK))
print("Folder Writable:", os.access(os.path.dirname(db_path), os.W_OK))
