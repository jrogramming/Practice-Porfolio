import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]]) # position and RGB value (h, w, rgb)
    # unsigned integer stored in 8 bits, never negative, 256 values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV) # convert to BGR to HSV

    hue = hsvC[0][0][0] # hue value

        # red hue wrap-around
            # hue is from 0 to 179 since OpenCV uses half-degree increments for the 360 degree color wheel
            # so red is at 0 and 179 but when detecting limits with a tolerance of 10

    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8) 
        upperLimit = np.array([180, 255, 255], dtype=np.uint8) # towards the pink range, the upper limit is manually capped at 180 because it's def red at that point

    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8) # towards the orange range, the lower limit is manually capped at 0 because it's def red with a hue under 15
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

        # 165 and 15 is because it absolutely prevents the need for special handling well (by 5) before the tolerance can send it outside 0 or 179.
        # the tolerance is 10, represented by the equation, on either side of the hue value, but close to the break in red the lower limit is 
        # capped at 0 and upper limit at 180 to avoid going out of bounds in the respective directions and bounds

        # notice saturation + value is above 100, otherwise it's too greyish or dark

    return lowerLimit, upperLimit