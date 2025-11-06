# 📂 FILE ORGANIZATION GUIDE

## How to Set Up Your Files on Windows

### 1. Create the Main Folder

Open File Explorer and create this folder:
```
C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
```

### 2. Download All Files

Download these files from the outputs folder and place them as shown below:

### 3. File Structure

Create this exact structure:

```
Meta-Aria-2/
│
├── setup_project.bat           ← Place this file here
├── requirements.txt            ← Place this file here
├── README.md                   ← Place this file here
├── QUICK_START.md             ← Place this file here
├── INSTALLATION_GUIDE.md      ← Place this file here
│
├── src/                        ← Create this folder
│   ├── main.py                ← Place this file inside src/
│   │
│   ├── detection/             ← Create this folder inside src/
│   │   ├── __init__.py        ← Rename detection__init__.py to __init__.py
│   │   └── aria_detector.py   ← Place this file inside detection/
│   │
│   ├── analysis/              ← Create this folder inside src/
│   │   ├── __init__.py        ← Rename analysis__init__.py to __init__.py
│   │   └── metrics_calculator.py ← Place this file inside analysis/
│   │
│   └── visualization/         ← Create this folder inside src/
│       ├── __init__.py        ← Rename visualization__init__.py to __init__.py
│       └── dashboard_generator.py ← Place this file inside visualization/
│
├── data/                       ← Create this folder (setup script will create subfolders)
├── outputs/                    ← Create this folder (setup script will create subfolders)
├── configs/                    ← Create this folder
└── venv/                       ← Will be created automatically by setup script
```

### 4. Step-by-Step File Placement

**Step 1: Create main folder**
- Create: `C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2`

**Step 2: Place root files**
Copy these to `Meta-Aria-2\`:
- setup_project.bat
- requirements.txt
- README.md
- QUICK_START.md
- INSTALLATION_GUIDE.md

**Step 3: Create src folder and place main.py**
- Create folder: `Meta-Aria-2\src\`
- Place `main.py` inside it

**Step 4: Create detection folder**
- Create folder: `Meta-Aria-2\src\detection\`
- Rename `detection__init__.py` to `__init__.py`
- Place `__init__.py` in the detection folder
- Place `aria_detector.py` in the detection folder

**Step 5: Create analysis folder**
- Create folder: `Meta-Aria-2\src\analysis\`
- Rename `analysis__init__.py` to `__init__.py`
- Place `__init__.py` in the analysis folder
- Place `metrics_calculator.py` in the analysis folder

**Step 6: Create visualization folder**
- Create folder: `Meta-Aria-2\src\visualization\`
- Rename `visualization__init__.py` to `__init__.py`
- Place `__init__.py` in the visualization folder
- Place `dashboard_generator.py` in the visualization folder

**Step 7: Create empty folders**
These will be populated by the setup script:
- Create: `Meta-Aria-2\data\`
- Create: `Meta-Aria-2\outputs\`
- Create: `Meta-Aria-2\configs\`

### 5. Verify Your Setup

Your final structure should look like this in File Explorer:

```
Meta-Aria-2
├── 📄 setup_project.bat
├── 📄 requirements.txt
├── 📄 README.md
├── 📄 QUICK_START.md
├── 📄 INSTALLATION_GUIDE.md
├── 📁 src
│   ├── 📄 main.py
│   ├── 📁 detection
│   │   ├── 📄 __init__.py
│   │   └── 📄 aria_detector.py
│   ├── 📁 analysis
│   │   ├── 📄 __init__.py
│   │   └── 📄 metrics_calculator.py
│   └── 📁 visualization
│       ├── 📄 __init__.py
│       └── 📄 dashboard_generator.py
├── 📁 data
├── 📁 outputs
└── 📁 configs
```

### 6. Run Setup

Once files are organized:
1. Double-click `setup_project.bat`
2. Wait for completion
3. Start using the system!

---

## Quick Copy-Paste Folder Creation (Command Prompt)

Open Command Prompt and run:

```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects
mkdir Meta-Aria-2
cd Meta-Aria-2
mkdir src
mkdir src\detection
mkdir src\analysis
mkdir src\visualization
mkdir data
mkdir outputs
mkdir configs
```

Then place your files in the appropriate folders as described above.

---

## File Descriptions

**Root Level:**
- `setup_project.bat` - One-time setup script
- `requirements.txt` - Python dependencies
- `README.md` - Full documentation
- `QUICK_START.md` - Quick reference guide
- `INSTALLATION_GUIDE.md` - Complete setup instructions

**src/main.py:**
- Main program entry point
- Handles command-line arguments
- Coordinates analysis workflow

**src/detection/aria_detector.py:**
- Loads .vrs recording files
- Extracts sensor data
- Handles visualization

**src/analysis/metrics_calculator.py:**
- Calculates motion metrics
- Analyzes stability
- Computes performance scores

**src/visualization/dashboard_generator.py:**
- Creates HTML reports
- Generates charts
- Produces performance summaries

**__init__.py files:**
- Make folders into Python packages
- Required for imports to work

---

## Common Mistakes to Avoid

❌ **Wrong:** Putting all files in root folder
✅ **Right:** Organize into src/ and subfolders

❌ **Wrong:** Forgetting __init__.py files
✅ **Right:** Each subfolder needs __init__.py

❌ **Wrong:** Wrong file names (detection_init.py)
✅ **Right:** Must be exactly __init__.py (two underscores on each side)

❌ **Wrong:** Files in wrong subfolders
✅ **Right:** Follow the structure exactly

---

## After Organization

Once files are organized correctly:

1. ✅ Double-click `setup_project.bat`
2. ✅ Wait for Python packages to install
3. ✅ Place your .vrs recordings in `data\recordings\`
4. ✅ Run analysis commands from Command Prompt
5. ✅ View results in `outputs\reports\`

---

## Checklist

Before running setup:
- [ ] All files downloaded
- [ ] Main folder created
- [ ] Root files in place
- [ ] src/ folder created with main.py
- [ ] detection/ folder created with files
- [ ] analysis/ folder created with files
- [ ] visualization/ folder created with files
- [ ] All __init__.py files renamed correctly
- [ ] Empty folders (data, outputs, configs) created

Ready to run setup? Double-click `setup_project.bat`!