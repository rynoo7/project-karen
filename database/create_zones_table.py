import sqlite3

conn = sqlite3.connect("/home/ryn007/Programs/Karen/garage.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS zones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER,
    type TEXT,
    label TEXT
)
""")

conn.commit()
conn.close()

print("Zones table created successfully.")
