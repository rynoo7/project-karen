import sqlite3
import os

db_path = "/home/ryn007/Programs/Karen/karen_garage.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    dimensions TEXT,
    function TEXT,
    photo_path TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    make TEXT,
    model TEXT,
    year TEXT,
    vin TEXT,
    manual_path TEXT,
    parts_list_path TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    quantity INTEGER,
    location TEXT,
    expiration_date TEXT
)
""")

conn.commit()
conn.close()
print(f"Database created at: {db_path}")
