import numpy as np
import argparse
from collections import deque
import cv2


# define the list of acceptable colors

boundaries = [
	([2,2,118], [40,40,255]) # works!
#	([34,34,178], [0, 0, 255]),
#	([25, 146, 190], [62, 174, 250]),
#	([103, 86, 65], [145, 133, 128])
]

pts = deque(maxlen = 1000)

def detect_object():
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        while True:
            gr, frame = cv2.VideoCapture(0).read()
            mask = cv2.inRange(frame, lower, upper)
            output = cv2.bitwise_and(frame, frame, mask = mask)
        #    cv2.imshow("images", np.hstack([frame, output]))
        #    cv2.imshow("images.png", output)
        #    cv2.imwrite('blueImage.png', output)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            if len(cnts) > 0:
                #print('multiple contours found')
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                try:
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                except ZeroDivisionError:
                    continue;   # leave this center
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
        #            cv2.imwrite("result.jpg", frame)
                pts.appendleft(center)
                for i in  xrange(1, len(pts)):
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    thickness = int(np.sqrt(1000/float(i+ 50)) * 1.5)
                    cv2.line(frame, pts[i-1], pts[i], (255,0,0), thickness)
                cv2.imshow("Frame", frame)
                #print("The frame is at = {0}".format(center))
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                #   print('break the loop')
                    break
            else:
                print('no contours found')
        