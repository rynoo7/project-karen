import sqlite3

db_path = "/home/ryn007/Programs/Karen/karen_garage.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tool_id = input("Enter the ID of the tool to delete: ").strip()

cursor.execute("DELETE FROM tools WHERE id = ?", (tool_id,))
conn.commit()

print(f"Deleted tool with ID: {tool_id}")
conn.close()
