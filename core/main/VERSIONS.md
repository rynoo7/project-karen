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
