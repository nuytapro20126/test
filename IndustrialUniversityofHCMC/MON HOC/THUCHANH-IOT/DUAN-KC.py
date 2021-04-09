import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
KNOWN_DISTANCE = 24.0
KNOWN_WIDTH = 11.0

def nothing(x):
    pass

def distance_to_camera(knownWidth,focalLength,perWidth):
  return (knownWidth * focalLength) / perWidth

def find_marker(frame):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)


def main():
    while True:
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        marker = find_marker(frame)
        focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

        #hsv xanh la cay - green
        lower_green = np.array([25, 52, 72])
        upper_green = np.array([102, 255, 255])

        #hsv xanh duong - blue
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        #mask xanh la cay - green
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        #mask xanh duong - blue
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

        #Gộp hsv 2 màu
        mask = cv2.bitwise_or(mask_green, mask_blue)
        target = cv2.bitwise_and(frame, frame, mask=mask)

        #Lọc nhiễu 2 màu
        kernel = np.ones((5, 5), np.uint8)
        mask1_green = cv2.erode(mask_green, kernel)
        mask1_blue = cv2.erode(mask_blue, kernel)
        # Contours detection
        if int(cv2.__version__[0]) > 3:
            # Opencv 4.x.x
            contours_blue, _ = cv2.findContours(mask1_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(mask1_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # Đọc contour đơn lẻ 2 màu

        else:
            # Opencv 3.x.x
            _, contours_blue, _ = cv2.findContours(mask1_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            _, contours_green, _ = cv2.findContours(mask1_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # Đọc contour đơn lẻ 2 màu

        # Trong vùng contour của hsv blue
        for cnt in contours_blue:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            M = cv2.moments(cnt)

            if M["m00"] != 0: # Xác định tâm
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cX, cY = 0, 0
            if area > 400:
                #if len(approx) == 3:
                #   cv2.putText(frame, "Triangle", (x, y), font, 1, (0))

                if len(approx) == 3:
                    cv2.putText(frame, "Triangle-Blue", (x, y), font, 1, (0))
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                    distance = distance_to_camera(KNOWN_WIDTH, focalLength, marker[0][1])
                    cv2.putText(frame, "%.2fcm" % (distance), (frame.shape[1] - 400, frame.shape[0] - 20),cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 2)

        for cnt in contours_green:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                # set values as what you need in the situation
                cX, cY = 0, 0
            if area > 400:
                # if len(approx) == 3:
                #   cv2.putText(frame, "Triangle", (x, y), font, 1, (0))

                if len(approx) == 4:
                    cv2.putText(frame, "Rectangle-Green", (x, y), font, 1, (0))
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                    distance = distance_to_camera(KNOWN_WIDTH, focalLength, marker[0][1])
                    cv2.putText(frame, "%.2fcm" % (distance), (frame.shape[1] - 400, frame.shape[0] - 20),
                          cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", target)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()