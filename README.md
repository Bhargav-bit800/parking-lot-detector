# Parking Lot Space Detector

A lightweight, camera-only smart parking system that runs on a Raspberry Pi using OpenCV.  
It combines adaptive MOG2 background subtraction with per-slot Laplacian checks and frame-count hysteresis to determine parking-slot occupancy in real time.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Directory Structure](#directory-structure)  
5. [Quick Start/How to Run](#quick-start)  
6. [Configuration](#configuration)  
7. [How It Works](#how-it-works) 
---

## Features

- **Hybrid Detection**: Combines MOG2 background subtraction with Laplacian-based edge analysis.  
- **Debounce Logic**: Per-slot enter/exit counters prevent flicker from transient noise.  
- **Interactive Coordinate Generator**: Click-to-define arbitrary slot polygons.  
- **Real-Time Visualization**: Draws colored contours and slot IDs on live video.  
- **Cross-Domain Testing**: Works on real CCTV (PKLot), CARLA simulator, online games, and DIY Hot Wheels setups.  

---

## Prerequisites

- **Python 3.7+**  
- **OpenCV** (`opencv-python`)  
- **NumPy**  
- **PyYAML**  
- **ffmpeg** (for frame extraction or format conversion)

Install Python dependencies via:

```bash
pip install opencv-python numpy pyyaml
```

---


## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Bhargav-bit800/smart-parking-detector.git
cd smart-parking-detector
pip install -r requirements.txt    # or: pip install opencv-python numpy pyyaml
```

---

## Directory Structure

```text
smart-parking-detector/
├── data/
│   └── coordinates.yml           # Slot definitions (YAML)
├── videos/
│   └── *.mp4                     # Example video files
├── parking_lot/                  # Python package (if installed)
│   ├── colors.py
│   ├── drawing_utils.py
│   ├── coordinates_generator.py
│   ├── motion_detector.py
│   └── __init__.py
├── detect_precision_hybrid.py    # Hybrid MOG2 + Laplacian detector
├── main.py                       # CLI for coordinate generation & Laplacian detector
├── setup.py
└── README.md
```
---
## Quick Start

### Create Images directory
```bash
mkdir -p images
```

### Extract a Reference Frame for coordinate generation
```bash
ffmpeg -i videos/your_video.mp4 \
       -vf "select=eq(n\,3)" \
       -vframes 1 \
       images/frame4.png

```
### Generate the Slot Coordinates
```bash
python3 main.py \
  --image images/frame4.png \
  --data  data/coordinates.yml \
  --video videos/your_video.mp4 \
  --start-frame 1

```
### Run the hybrid MOG2+Laplacian Detector
```bash
python3 detect_precision_hybrid.py

```
---
## Configuration
Edit the constants at the top of detect_precision_hybrid.py:
```bash
VIDEO_PATH      = "videos/your_video.mp4"
COORDS_YAML     = "data/coordinates.yml"
MOTION_HISTORY  = 500         # frames MOG2 remembers
FG_THRESHOLD    = 200         # mask binarization threshold (0–255)
ENTER_THRESH    = 0.02        # >2% moving pixels → enter candidate
EXIT_THRESH     = 0.005       # <0.5% moving pixels → exit candidate
ENTER_FRAMES    = 5           # frames above ENTER_THRESH to confirm occupancy
EXIT_FRAMES     = 5           # frames below EXIT_THRESH to confirm vacancy
``` 
---

## How It Works
### MOG2 Background Subtraction
Models each pixel as a mixture of Gaussians to produce an adaptive foreground mask, suppressing shadows and lighting changes.
### Mask Cleanup
Thresholds the mask at FG_THRESHOLD and applies morphological open/close to remove noise.
### Per-Slot Analysis
Computes the fraction of moving pixels inside each slot polygon and uses enter/exit counters with hysteresis for stable state transitions.
### Visualization
Overlays red (occupied) or green (vacant) contours and slot IDs, and displays the annotated frame in real time with OpenCV’s imshow().




---


   

   






