# 🚀 Quick Start Guide - Meta Aria 2 Surgical Training

## For First-Time Users

### 1️⃣ Install Python (One-Time Setup)

Download and install Python 3.11 from: https://www.python.org/downloads/

⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation!

### 2️⃣ Set Up Project (One-Time Setup)

Open Command Prompt:
- Press `Win + R`
- Type `cmd` and press Enter

Run these commands:
```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
setup_project.bat
```

Wait 5-10 minutes for installation to complete.

### 3️⃣ Record Training Session

Using your Meta Aria 2 glasses:
1. Open Meta Aria app on your phone
2. Start recording
3. Perform surgical training
4. Stop recording
5. Export recording to your phone

### 4️⃣ Transfer Recording to PC

**Option A - Via USB:**
- Connect phone to PC
- Copy `.vrs` file to: `C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2\data\recordings\`

**Option B - Cloud:**
- Upload to OneDrive/Google Drive from phone
- Download to PC
- Move to `data\recordings\` folder

### 5️⃣ Run Analysis

Open Command Prompt and run:
```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
venv\Scripts\activate.bat
python src\main.py --recording data\recordings\YOUR_FILE.vrs --visualize
```

Replace `YOUR_FILE.vrs` with your actual filename.

### 6️⃣ View Results

After analysis completes:
1. Navigate to: `outputs\reports\`
2. Open the newest folder
3. Double-click `report.html`
4. View your performance metrics!

---

## Quick Commands Reference

### Every Time You Want to Analyze

```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
venv\Scripts\activate.bat
```

Then run ONE of these:

**Analyze single file:**
```cmd
python src\main.py --recording data\recordings\session1.vrs
```

**Analyze with visualization:**
```cmd
python src\main.py --recording data\recordings\session1.vrs --visualize
```

**Analyze all files:**
```cmd
python src\main.py --mode batch
```

---

## What You'll Get

✅ **Overall Performance Score** (0-100)
✅ **Head Stability Analysis** (tremor, movement)
✅ **Stress Indicators** (heart rate estimation)
✅ **Visual Charts** (motion, stress, performance)
✅ **Personalized Recommendations**

---

## Troubleshooting

**Problem: "Python is not recognized"**
- Solution: Reinstall Python with "Add to PATH" checked

**Problem: "No recordings found"**
- Solution: Make sure .vrs files are in `data\recordings\` folder

**Problem: "Module not found"**
- Solution: Activate environment first:
  ```cmd
  venv\Scripts\activate.bat
  ```

---

## File Naming Tips

Name your recordings descriptively:
- `coronary_bypass_session1.vrs`
- `suturing_practice_2024-11-06.vrs`
- `beginner_training_day1.vrs`

This helps track progress over time!

---

## Next Session Workflow

1. Record new session on Aria glasses
2. Transfer .vrs file to `data\recordings\`
3. Run: `python src\main.py --recording data\recordings\NEW_FILE.vrs`
4. Compare results with previous sessions
5. Focus on improving weak areas

---

## Need Help?

1. Read the full README.md
2. Check error messages
3. Verify .vrs file is valid
4. Try a shorter test recording first