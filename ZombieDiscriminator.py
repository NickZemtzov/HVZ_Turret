import cv2
import numpy as np
import serial
import time

# Arduino Communication
arduino=serial.Serial(port='/dev/cu.usbserial-14230', baudrate=115200, timeout=0.1)
HorizontalPosition = 0
VerticalPosition = 60
VerticalConfines = (30,85)

def SendCommand(sent, expected):
    sent = bytes(sent,'utf-8')
    expected = bytes(str(ord(expected)),'utf-8')
    print(f"Sending {sent}, expected {expected}.")
    arduino.write(sent)
    data = bytes("", 'utf-8')
    now = time.time()
    while data != expected:
        #try:
        data = arduino.readline()
        if time.time() > now+5:
            return 60
        #except:
        #    arduino=serial.Serial(port='/dev/cu.usbserial-14230', baudrate=115200, timeout=0.1)
            #time.sleep(2)
    print(data.decode('utf-8'))
    return int(data.decode('utf-8'))

def CreateCommand(horizontal_delta, vertical_delta):
    global VerticalPosition
    global HorizontalPosition
    global VerticalConfines
    # Vertical Movement
    vertical_weight = 2
    print(vertical_delta)
    if vertical_delta > 10: # if person is far enoughbelow where aiming move down
        new_position = int(VerticalPosition - vertical_delta/vertical_weight)
        if new_position < VerticalConfines[0]:
            new_position = VerticalConfines[0]
        VerticalPosition = SendCommand(f"4{chr(new_position)}", chr(new_position))
    elif vertical_delta < -10: # or likewise move up
        new_position = int(VerticalPosition - vertical_delta/vertical_weight)
        if new_position > VerticalConfines[1]:
            new_position = VerticalConfines[1]
        VerticalPosition = SendCommand(f"4{chr(new_position)}", chr(new_position))
    

    elif vertical_delta < 10 and vertical_delta > -10 and horizontal_delta < 10 and horizontal_delta > -10:
        SendCommand("3", "3")
    



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
    # Camera setup
    ret, image = cap.read()
    image = cv2.resize(image,(0,0), fx=scalingFactor, fy=scalingFactor)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    frame_center = (int(image.shape[1]/2), int(image.shape[0]/2))            # You should hard code this as a variable for the specific camera
    upper_body = torso_cascade.detectMultiScale(gray, 1.1, 8)

    # Find the zombies
    Zombies = []
    for (x, y, w, h) in upper_body:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped_image = image[y:y+h, x:x+w]
        hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (80,150,0), (170,255,255)) # Takes HSV color
        #cv2.imshow('mask color', mask)
        if int(np.sum(mask == 255)/(w*h)*1000) > LowerMaskThreashold and int(np.sum(mask == 255)/(w*h)*1000) < UpperMaskThreashold:
            cv2.putText(image, 'Zombie', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 3, cv2.LINE_AA)
            Zombies.append([x,y,w,h])

    # Find the closest zombie by how large it's rectangle is and paint a target
    if len(Zombies) > 0:
        target = sorted(Zombies, key=lambda x:x[2]*x[3], reverse=True)[0] # Finds the closest ZombieA
        target_center = (int(target[0]+(target[2]/2)), int(target[1]+(target[3]/2)))
        cv2.line(image, target_center, frame_center, (0, 0, 255), 3)

        # Determine what commands to send to the Arduino based on zombie location and persistence
        horizontal_delta = frame_center[0] - target_center[0]
        vertical_delta = frame_center[1] - target_center[1]

        CreateCommand(horizontal_delta, vertical_delta)


    cv2.imshow('Frame',image)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
