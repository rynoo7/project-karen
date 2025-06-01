import sqlite3

db_path = "/home/ryn007/Programs/Karen/karen_garage.db"

# Sample tool data
tool_data = {
    "name": "Torque Wrench",
    "location": "BallBearing Toolbox - Drawer 2",
    "dimensions": "18 in × 1.5 in × 1.5 in",
    "function": "Applies precise torque to fasteners",
    "photo_path": "/home/ryn007/Programs/Karen/Photos/Torque_Wrench.jpg"
}

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert the data
cursor.execute("""
    INSERT INTO tools (name, location, dimensions, function, photo_path)
    VALUES (:name, :location, :dimensions, :function, :photo_path)
""", tool_data)

conn.commit()
conn.close()

print(f"Tool '{tool_data['name']}' added successfully!")
