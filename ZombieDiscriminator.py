import cv2
import numpy as np

# Do bitwise input over SPI

#Camera setup
cap = cv2.VideoCapture(0)

##########################################
#Hyperparameters
##########################################

# This is the factor by which the image is scaled in preprocessing.
# The image must maintain proportions for detection to work properly.
scalingFactor = 0.5

# This is the range of color in HSV for the mask. It's currently set to blue.
darker_shade = (80,150,0)
lighter_shade = (170,255,255)

# The proportion of the pixels that are the correct shade * 1000.
LowerMaskThreashold = 10
UpperMaskThreashold = 100

# Uses an upper body detector cuz that worked best at all angles
torso_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')

while(True):
    ret, image = cap.read()
    image = cv2.resize(image,(0,0), fx=scalingFactor, fy=scalingFactor)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    frameCenter = (int(image.shape[1]/2), int(image.shape[0]/2))            # You should hard code this as a variable for the specific camera
    upper_body = torso_cascade.detectMultiScale(gray, 1.1, 8)

    # Location of the target.
    # Lateral options: left, right, no move. 2 bits
    # Vertical options: left, right, no move. 2 bits
    vertical

    Zombies = []
    for (x, y, w, h) in upper_body:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped_image = image[y:y+h, x:x+w]
        hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (80,150,0), (170,255,255)) # Takes HSV color
        #cv2.imshow('mask red color', mask)
        if int(np.sum(mask == 255)/(w*h)*1000) > LowerMaskThreashold and int(np.sum(mask == 255)/(w*h)*1000) < UpperMaskThreashold:
            cv2.putText(image, 'Zombie', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 3, cv2.LINE_AA)
            Zombies.append([x,y,w,h])

    if len(Zombies) > 0:
        target = sorted(Zombies, key=lambda x:x[2]*x[3], reverse=True)[0] # Finds the closest Zombie

        # Determine which way the servo should move





    cv2.imshow('Frame',image)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
