# Karen Core: Version History

This document tracks the evolution of core Karen modules. Each entry captures the purpose, changes, and authorship of a major version.

---

## karen-core-v2.0.py

**Author:** Ryan  
**Branch of Origin:** karen_2.0.py  
**Created:** [Phase 2 Start Date]

### Summary:
A refined, modular rewrite of Karen's interactive garage interface. This version introduces dynamic zone rendering, cursor-based interaction, and optional snapshot capturing using OpenCV.

### Key Additions:
- Added `cv2`, `sqlite3`, and `numpy` imports
- Added `InteractiveZone` class:
  - Supports hover highlighting
  - Responds to cursor clicks with dynamic behavior
- Snapshot function that saves a frame when a specific zone is clicked
- Structured, reusable functions replacing inline logic

### Notes:
This version is meant to replace `karen_2.0.py` as the foundation for all future garage interface development.


---

## [2025-06-02] Assets Folder Overhaul

- 🎨 Moved all media files (photos, calibration frames, snapshots, and recordings) into the new `assets/` directory
- 🧭 Created subfolders: `Calibration/`, `Photos/`, `Recordings/`, `snapshots/`
- 🪪 Added `README.md` to explain the structure and purpose of `assets/`
- ✅ Cleaned up misfiled assets from other folders


### [tools/] Folder - Initial Documentation

- Verified and documented `delete_tool.py` and `search_tool.py`
- Added new README with descriptions and usage details


### [2025-06-02] Lynnsanity
- 🛠 Updated `karen_calibrate.py` to reflect new assets path:
  `/home/lynnsanity/Karen/assets/Calibration` replaces hardcoded `/home/ryn007/...`


### [2025-06-02] Organized data/ Folder

- 📦 Confirmed layout and use of `data/zones/` for zone export files
- 🧾 Added `README.md` to clarify its purpose as a raw data container
 - still trying to remember how to open and edit this thing without asking...fucking nano thing

## [2025-06-02] Folder Organization: Database

- 🧰 Moved all database scripts into `/database/`
- 🧾 Created README for database folder
- 🧠 Left active user-facing scripts like `search_tool.py` and `delete_tool.py` in `/tools/` for now

 - definitely did NOT learn how to launch this window without asking, actually opened an empty version somehow that we now can't find? If you see that, no you didn't. 


## [2025-06-02] Assets Directory Established

- 🧰 Standardized asset folders:
  - `Calibration/` for camera alignment reference frames
  - `Photos/` for UI-linked visual assets
  - `Recordings/` for video/audio sessions
  - `snapshots/` for automated memory capture frames
- 🧼 Moved any loose assets into correct subfolders
- 🗂️ Confirmed directory integrity for cross-module linking
- opened it ALMOST without looking...also I might have already done this for assets, or maybe I just did a preliminary organization...I can't remember. moving right along..."


- 🖼️ Verified asset hygiene — confirmed all image and video files live inside `/assets/`; none floating outside.
- boo yah baby

- 🧹 Emptied `chatty_files/` — confirmed it only contains temporary transfer files and is now clean.
- this feels like a redudant log entry, but hey I love a good back-patting as much as the next guy (shrug)
