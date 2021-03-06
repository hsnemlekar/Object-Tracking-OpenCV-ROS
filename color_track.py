# NOT a ROS executable

# Detects Orange object

import cv2
import numpy as np  # np is used for array functions
import imutils  # image processing functions

cam = cv2.VideoCapture(0)


while True:
	(val, frame) = cam.read()  # val gives 1 if frame is successfully read
	if not val:
		break
	
	lower = np.array([0, 100, 50])
	upper = np.array([10, 100, 100])
	colors = np.array([0, 0, 255])

	frame = imutils.resize(frame, width=700)  # frame size
	blurred = cv2.GaussianBlur(frame, (7, 7), 0)  # removes noise #(7,7) is the size on which blur is applied at a time
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)  # change input frame to HSV

	kernel = np.ones((9, 9), np.uint8)
	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # erosion followed by dilation
	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # dilation followed by erosion

	# RETR_EXTERNAL is the mode, CHAIN_APPROX_SIMPLE is the method, [-2] is the offset
	contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	if len(contour)>0:
		c = max(contour, key=cv2.contourArea)
		(x,y), radius = cv2.minEnclosingCircle(c)

		# Moments
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# Specify min size of object to be detected
		if radius > 1:
			cv2.circle(frame, (int(x), int(y)), int(radius), colors, 2)
			cv2.putText(frame, "OBJECT", (int(x - (radius+1)), int(y - (radius+1))), cv2.FONT_HERSHEY_COMPLEX, 0.8, colors, 2)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
	    break

cam.release()
cv2.destroyAllWindows()
