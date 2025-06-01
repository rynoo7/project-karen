import sqlite3

db_path = "/home/ryn007/Programs/Karen/karen_garage.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, name, location, dimensions, function, photo_path FROM tools")
tools = cursor.fetchall()

if not tools:
    print("No tools found in the database.")
else:
    for tool in tools:
        print(f"""
ID:         {tool[0]}
Name:       {tool[1]}
Location:   {tool[2]}
Size:       {tool[3]}
Function:   {tool[4]}
Photo:      {tool[5]}
------------------------
""")

conn.close()
