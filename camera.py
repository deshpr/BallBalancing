import cv2

c = cv2.VideoCapture(0)
while True:
	_, frame = c.read()
	cv2.imshow("res", frame)	
	cv2.waitKey(1)
