import cv2
import math
import numpy as np
import pandas as pd
import matplotlib
from pathlib import Path
from parallelencode import run

ix, iy, k = 200, 200, 1


def on_mouse(event, x, y, flag, param):
    global ix, iy, k
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        k = -1


cv2.namedWindow("window")
cv2.setMouseCallback("window", on_mouse)
cap = cv2.VideoCapture(0)
while True:
    _, frm = cap.read()
    cv2.imshow("window", frm)
    if cv2.waitKey(1) == 27 or k == -1:
        old_gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        cap.release()
        cv2.destroyAllWindows()
        break

old_pts = np.array([[ix, iy]], dtype="float32").reshape(-1, 1, 2)
mask = np.zeros_like(frm)

while True:
    _, frame2 = cap.read()
    new_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    new_pts, status, error = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, old_pts, None, maxLevel=1, criteria=(
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08))

    cv2.circle(mask, (int(new_pts.ravel()[0]),
               int(new_pts.ravel()[1])), 2, (0, 255, 0), 2)
    combined = cv2.addWeighted(frame2, 0.7, mask, 0.3, 0.1)
    cv2.imshow("new win", mask)
    cv2.imshow("wind", combined)
    old_gray = new_gray.copy()
    old_pts = new_pts.copy()

    if cv2.waitKey(1) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
