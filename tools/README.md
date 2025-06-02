# Karen Tools Scripts

This folder contains standalone utility scripts that directly interact with Karen's garage database (`karen_garage.db`).

---

## 🔧 Scripts

| Script           | Purpose                                           |
|------------------|---------------------------------------------------|
| `delete_tool.py` | Deletes a tool from the database by its ID.       |
| `search_tool.py` | Searches for tools in the database by name.       |

---

## 🧠 Notes

- Both scripts directly connect to the SQLite database.
- Database path must be updated if running from a different location.
- Use caution when running `delete_tool.py` — it permanently removes data without confirmation.

---

Happy querying!
