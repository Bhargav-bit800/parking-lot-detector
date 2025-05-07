#!/usr/bin/env python3
import cv2
import yaml
import numpy as np
from drawing_utils import draw_contours
from colors import COLOR_RED, COLOR_GREEN, COLOR_WHITE

# ─── CONFIG ───────────────────────────────────────────────────────────────
VIDEO_PATH    = "videos/vehicles_carla1.mp4"
COORDS_YAML   = "data/coordinates.yml"

# Background subtractor history
MOTION_HISTORY = 500

# Foreground mask cleanup
FG_THRESHOLD   = 200   # binarize at 200/255
OPEN_KER       = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
CLOSE_KER      = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

# Percent‐of‐pixels thresholds
ENTER_THRESH   = 0.02  # >2% motion → candidate to occupy
EXIT_THRESH    = 0.005 # <0.5% motion → candidate to empty

# Debounce frame counts
ENTER_FRAMES   = 5     # need 5 consecutive “enter” frames
EXIT_FRAMES    = 5     # need 5 consecutive “exit” frames
# ────────────────────────────────────────────────────────────────────────────

def main():
    # 1) Load slots & initial flags
    slots = yaml.safe_load(open(COORDS_YAML))
    statuses   = [p.get("occupied", False) for p in slots]
    enter_cnts = [0]*len(slots)
    exit_cnts  = [0]*len(slots)

    # 2) Build contours + bounding‐rects
    contours, rects = [], []
    for p in slots:
        pts = np.array(p["coordinates"], dtype=np.int32)
        contours.append(pts)
        rects.append(cv2.boundingRect(pts))  # x,y,w,h

    # 3) Video + background subtractor
    cap    = cv2.VideoCapture(VIDEO_PATH)
    backSub = cv2.createBackgroundSubtractorMOG2(
        history=MOTION_HISTORY, varThreshold=16, detectShadows=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        disp    = frame.copy()
        fg_mask = backSub.apply(frame)

        # 4) Clean up the FG mask
        _, fg_mask = cv2.threshold(fg_mask, FG_THRESHOLD, 255, cv2.THRESH_BINARY)
        fg_mask    = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN,  OPEN_KER)
        fg_mask    = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, CLOSE_KER)

        # 5) Per‐slot decision with hysteresis + debounce
        for i, pts in enumerate(contours):
            x,y,w,h = rects[i]
            slot_fg = fg_mask[y:y+h, x:x+w]
            pct     = cv2.countNonZero(slot_fg) / float(w*h)

            if not statuses[i]:
                # currently empty → look for ENTER 
                if pct > ENTER_THRESH:
                    enter_cnts[i] += 1
                    exit_cnts[i]  = 0
                    if enter_cnts[i] >= ENTER_FRAMES:
                        statuses[i]    = True
                        enter_cnts[i]  = 0
                else:
                    enter_cnts[i] = 0
            else:
                # currently occupied → look for EXIT
                if pct < EXIT_THRESH:
                    exit_cnts[i] += 1
                    enter_cnts[i] = 0
                    if exit_cnts[i] >= EXIT_FRAMES:
                        statuses[i]   = False
                        exit_cnts[i]  = 0
                else:
                    exit_cnts[i] = 0

            # 6) Draw result
            color = COLOR_RED if statuses[i] else COLOR_GREEN
            draw_contours(disp, pts, str(slots[i]["id"]+1),
                          COLOR_WHITE, color)

        cv2.imshow("Precision Hybrid Detector", disp)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
