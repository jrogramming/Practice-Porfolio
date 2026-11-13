import cv2 
from PIL import Image
# Python image-processing library
from util import get_limits

capture = cv2.VideoCapture(0)

purple = (128, 0, 128) # BGR value for purple so get_limits can do the math for what

while True:
    ret, frame = capture.read()
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert to HSV

    lowerLimit, upperLimit = get_limits(purple)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit) # mask for the color purple
    mask_ = Image.fromarray(mask) # convert to PIL image

    bbox = mask_.getbbox() # bounding box of mask, draws a rectangle around the detected color region

    if bbox is not None: # it exists / detects something

        x1, y1, x2, y2 = bbox # unpack the bounding box coordinates
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame) # show the frame with the bounding box

    if cv2.waitKey(1) & 0xFF == ord('q'): # press 'q' to quit
        break

        capture.release() # release the capture object
        cv2.destroyAllWindows() # close, done!
        