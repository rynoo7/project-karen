# Karen: Core Modules Overview

Welcome to the beating heart of Karen's AI system! This folder contains the primary Python files responsible for processing, interacting with, and evolving Karen’s core logic.

---

## 🚂 Purpose

The `core/` directory houses all major scripts related to Karen’s internal operations, including garage mapping, sprite interactions, system control logic, and UI behavior. If you're looking to understand or expand Karen's mind, this is where you start.

---

## 📁 Folder Structure

This folder is split into three areas to make collaboration and experimentation easier:

* `main/` – The most current, production-level code
* `experimental/` – In-progress or alternate feature branches
* `archive/` – Older versions kept for historical reference or code recovery

---

## 🧠 Primary Files (in `main/`)

| File Name            | Purpose                                                                                |
| -------------------- | -------------------------------------------------------------------------------------- |
| `karen-core-v2.0.py` | Stable rewrite of `karen_2.0.py`. Introduces dynamic sprite zones and snapshot saving. |
| `karen-core-v2.1.py` | In-progress version possibly meant to replace v2.0. Needs review and testing.          |
| `karen_2.0.py`       | Original second-gen file before cleanup. Legacy.                                       |
| `bk.py`              | Possibly base kernel or shorthand entry point. Content TBD.                            |

Refer to `VERSIONS.md` for detailed diffs and history tracking!

---

## 🛠️ Dependencies

Make sure the following packages are installed before running any files in this folder:

```bash
sudo apt install python3-pygame python3-opencv python3-numpy python3-sqlite
```

---

## 🚀 Running Karen

In the terminal, navigate to the core directory and run the main file:

```bash
cd ~/Karen/core/main
python3 karen-core-v2.0.py
```

(Adjust the filename depending on what version you’re working with.)

---

## ✅ Contributing

When working on this folder:

1. Create new versions inside the `experimental/` folder first
2. Log major updates in `VERSIONS.md`
3. Rename stable files and move them to `main/` when ready

---

## 📓 Notes

* All legacy versions are kept in `archive/`
* Future plan: Merge interactive zones with video memory tools
* Consider linking to the database tool from the garage\_ui folder

---

Happy tinkering — this is where Karen comes to life!

> "She’s more than just code. She’s memory, curiosity, and chaos in harmony."
