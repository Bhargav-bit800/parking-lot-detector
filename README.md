# Parking Lot Space Detector

A lightweight, camera-only smart parking system that runs on a Raspberry Pi using OpenCV.  
It combines adaptive MOG2 background subtraction with per-slot Laplacian checks and frame-count hysteresis to determine parking-slot occupancy in real time.

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Directory Structure](#directory-structure)  
5. [Quick Start](#quick-start)  
   - [0) Prepare Video / Extract Frame with ffmpeg](#0-prepare-video--extract-frame-with-ffmpeg)  
   - [1) Generate Slot Coordinates](#1-generate-slot-coordinates)  
   - [2) Run Laplacian-Only Detector](#2-run-laplacian-only-detector)  
   - [3) Run Hybrid MOG2 Detector](#3-run-hybrid-mog2-detector)  
6. [Configuration](#configuration)  
7. [How It Works](#how-it-works)  
8. [Extending & Packaging](#extending--packaging)  
9. [License](#license)  

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

1. **Create images directory** (one-time setup):
   ```bash
   mkdir -p images
   ```
2. **Extract a reference frame for coordinate generation** :

 ffmpeg -i videos/your_video.mp4 \
       -vf "select=eq(n\,3)" \
       -vframes 1 \
       images/frame4.png
  
3. **Generate slot coordinates** :
   
python3 main.py \
  --image images/frame4.png \
  --data  data/coordinates.yml \
  --video videos/vehicles_carla1.mp4 \
  --start-frame 1
   

4. **Run the hybrid MOG2+Laplacian Detector** :

python3 detect_precision_hybrid.py

   ```

---
   

   






