import sqlite3

db_path = "/home/ryn007/Programs/Karen/karen_garage.db"
search_term = input("Enter part of the tool name to search: ").strip()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT id, name, location, dimensions, function, photo_path
    FROM tools
    WHERE name LIKE ?
""", (f"%{search_term}%",))

results = cursor.fetchall()

if not results:
    print("No matching tools found.")
else:
    for tool in results:
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
