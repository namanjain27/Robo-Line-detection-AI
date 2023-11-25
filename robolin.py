import cv2
import numpy as np
import sys
if(len(sys.argv) != 2):
    print("Incorrect argument given. Usage: gutter.py <location>")
    exit(1)
loc = sys.argv[1]
n = ""
for s in loc:
    if s.isdigit():
        n += s
img = cv2.imread(loc)
img0 = cv2.bilateralFilter(img, 3, 75, 75)
bandw = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
v = np.median(bandw)
sigma = 0.33
lower_thresh = int(max(0, (1.0 - sigma) * v))
upper_thresh = int(min(255, (1.0 + sigma) * v))
cannyimg = cv2.Canny(bandw, lower_thresh, upper_thresh, apertureSize=3)
lines = cv2.HoughLines(cannyimg, 1, np.pi/120, 150)
for line in lines:
    c, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*c
    y0 = b*c
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

cv2.imwrite('robolin-tiles'+n+'.jpg', img)
