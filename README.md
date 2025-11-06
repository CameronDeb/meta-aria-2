# Meta Aria 2 Surgical Training Analysis System

Complete system for analyzing surgical training sessions using Meta Aria 2 smart glasses.

## 🎯 Project Overview

This system captures and analyzes surgical training data from Meta Aria 2 glasses including:
- **Motion tracking** (head stability, tremor analysis)
- **Visual analysis** (focus, stability)
- **Stress monitoring** (heart rate, performance under pressure)
- **Performance metrics** (overall skill assessment)

## 📋 Prerequisites

### Hardware
- **Meta Aria 2 smart glasses** with recording capability
- **Windows PC** (Windows 10 or later)
- **USB-C cable** for data transfer

### Software
- **Python 3.9, 3.10, or 3.11** (NOT 3.12+)
- **Meta Aria Mobile App** installed on your phone

## 🚀 Installation Guide

### Step 1: Install Python

1. Go to [python.org](https://www.python.org/downloads/)
2. Download **Python 3.11** (recommended)
3. During installation, **CHECK** "Add Python to PATH"
4. Complete the installation

Verify installation:
```cmd
python --version
```

### Step 2: Set Up the Project

1. Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter)

2. Navigate to the project directory:
```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
```

3. Run the setup script:
```cmd
setup_project.bat
```

This will:
- Create necessary directories
- Set up a Python virtual environment
- Install all required packages (takes 5-10 minutes)

## 📱 Recording Data with Meta Aria 2

### Method 1: Using the Meta Aria Mobile App (Recommended)

1. **Pair your glasses** with your phone via the Meta Aria app
2. **Start a recording** in the app during surgical training
3. **Stop the recording** when finished
4. **Export the recording**:
   - Open the Meta Aria app
   - Go to Recordings
   - Select your recording
   - Tap "Export" or "Download"
   - Choose "Save to Files" or transfer to PC

5. **Transfer to PC**:
   - Connect phone to PC via USB
   - Copy the `.vrs` file from phone to:
     ```
     C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2\data\recordings\
     ```

### Method 2: Direct USB Transfer

1. Connect Aria glasses to PC via USB-C
2. Glasses will appear as a storage device
3. Navigate to recordings folder
4. Copy `.vrs` files to:
   ```
   C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2\data\recordings\
   ```

## 🖥️ Running the Analysis

### Activate the Environment

Every time you open a new Command Prompt, activate the virtual environment:

```cmd
cd C:\Users\Owner\OneDrive\Documents\Projects\Meta-Aria-2
venv\Scripts\activate.bat
```

You should see `(venv)` at the start of your command prompt.

### Analyze a Single Recording

```cmd
python src\main.py --recording data\recordings\your_session.vrs --visualize
```

Replace `your_session.vrs` with your actual filename.

### Analyze All Recordings in the Directory

```cmd
python src\main.py --mode batch --recordings-dir data\recordings --visualize
```

### Analysis Options

```cmd
# Basic analysis (no visualization)
python src\main.py --recording data\recordings\session1.vrs

# With live visualization
python src\main.py --recording data\recordings\session1.vrs --visualize

# Custom output directory
python src\main.py --recording data\recordings\session1.vrs --output-dir outputs\my_analysis

# Batch process all recordings
python src\main.py --mode batch --visualize
```

## 📊 Understanding the Output

After analysis, you'll find:

```
outputs/
  reports/
    session_name_20241106_143022/
      ├── report.html          # Interactive HTML report
      ├── metrics.json         # Raw metrics data
      └── charts/
          ├── motion_analysis.png
          ├── stress_analysis.png
          └── performance_radar.png
```

### Opening the Report

1. Navigate to the output folder
2. Double-click `report.html`
3. Opens in your web browser with:
   - Overall performance score
   - Motion and stability metrics
   - Stress indicators
   - Interactive charts
   - Recommendations

## 📁 Project Structure

```
Meta-Aria-2/
├── data/
│   ├── recordings/          # Place your .vrs files here
│   ├── processed/           # Processed data cache
│   └── models/              # Custom detection models (optional)
│
├── src/
│   ├── main.py             # Main entry point
│   ├── detection/
│   │   └── aria_detector.py
│   ├── analysis/
│   │   └── metrics_calculator.py
│   └── visualization/
│       └── dashboard_generator.py
│
├── outputs/
│   ├── reports/            # Generated analysis reports
│   └── videos/             # Exported video clips
│
├── venv/                   # Virtual environment (auto-created)
├── setup_project.bat       # Setup script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Troubleshooting

### "Python is not recognized"
- Reinstall Python and check "Add to PATH"
- Or manually add Python to PATH

### "No module named 'projectaria_tools'"
```cmd
venv\Scripts\activate.bat
pip install projectaria-tools
```

### "No .vrs files found"
- Make sure you placed recordings in `data\recordings\`
- Check file extension is `.vrs` not `.VRS` or other

### Visualization not working
```cmd
pip install rerun-sdk
```

### Recording file won't load
- Ensure file isn't corrupted
- Try recording a new shorter session (30 seconds)
- Check Meta Aria app for export options

## 📈 Measured Metrics

### Motion Metrics
- **Head Stability Score** (0-10): How steady the head position is
- **Average Tremor**: Magnitude of hand/head trembling
- **Movement Patterns**: Total head movement during procedure

### Stability Metrics
- **Visual Stability** (0-10): Frame-to-frame consistency
- **Focus Score**: Estimated focus quality
- **Frame Jitter**: Camera shake measurement

### Stress Metrics
- **Heart Rate**: Average BPM during session (when available)
- **Peak Stress Level** (0-10): Maximum stress indicator
- **Stress-Performance Correlation**: How stress affects accuracy

### Performance Metrics
- **Overall Score** (0-100): Weighted performance rating
- **Technical Skill**: Motion + stability combined
- **Stress Management**: Ability to perform under pressure
- **Consistency**: Steadiness throughout session

## 🎓 Next Steps

1. **Record baseline session**: Record a standard training procedure
2. **Analyze regularly**: Process recordings after each training session
3. **Track progress**: Compare metrics across sessions
4. **Identify patterns**: Notice when stress affects performance
5. **Improve systematically**: Focus on specific weak areas

## 🤝 Advanced Usage

### Custom Tool Detection (Optional)

To add surgical tool detection:

1. Uncomment ML libraries in `requirements.txt`
2. Install:
   ```cmd
   pip install torch torchvision transformers
   ```
3. Run with detection:
   ```cmd
   python src\main.py --recording session.vrs --detect-tools
   ```

### Live Streaming Analysis (Future)

Currently, this analyzes recorded sessions. For live analysis:
- Use Meta Aria's livestreaming feature
- Process frames in real-time
- Provide immediate audio feedback

## 📞 Support

If you encounter issues:
1. Check this README
2. Review error messages carefully
3. Ensure all prerequisites are met
4. Try with a fresh recording

## 📄 License

This project is for research and educational purposes.
Meta Aria is a trademark of Meta Platforms, Inc."# meta-aria-2" 
