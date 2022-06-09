import cv2
import numpy as np
import serial
import time
arduino = serial.Serial(port='/dev/cu.usbserial-14330', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value
#Facial recognition with bandana to find Zombies

#find the center of the largest each rectangle and use that to find velocity. You have to account for motion
# of the platform as well though so this may not be possible

#Camera setup
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

##########################################
#Hyperparameters
##########################################

# This is the factor by which the image is scaled in preprocessing.
# The image must maintain proportions for facial detection to work properly.
scalingFactor = 0.5

# This is the BGR value of the zombie bandana.
# It is currently set to the color of my running shorts taken with average ambient light.
bandanaBGR = [88, 45, 15]

# This is the range each BGR value must fall within to be counted.
# For example if bandanaBGR[0] == 170 then any pixel whose B value is between 150 and 190 would be counted.
approxFactor = 30

# These are the areas above and below the face that is scanned for bandana colors.
aboveFaceFactor = 0.2
belowTopOfFaceFactor = 0.05

# This is the minimum proportion of pixels that are bandana colored in the scanned area for somthing to be counted as a zombie.
matchThreashold = 0.1

#
bodyShotFactor = 0.5


while True:
    # Camera setup
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    frame = cv2.resize(frame,(0,0), fx=scalingFactor, fy=scalingFactor)


    ZombieLocation = [0,0]
    #finds closest face and classify if it's a zombie. NOTE THIS! It only cares about the closest face for computational speed.
    # If better detection is needed its a simple matter to change this script to search until it finds a zombie, but the frame rate may suffer
    closest = -1
    index = 0
    for face in range(len(faces)):
        if faces[face][2]*faces[face][3] > closest:
            closest = faces[face][2]*faces[face][3]
            index = face
    if closest != -1:
        x,y,w,h = faces[index][0],faces[index][1],faces[index][2],faces[index][3]
        x = int(x*scalingFactor)
        y = int(y*scalingFactor)
        w = int(w*scalingFactor)
        h = int(h*scalingFactor)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)

        count = 0
        for row in range(y-int(h*aboveFaceFactor),y+int(h*belowTopOfFaceFactor)):
            for col in range(x,x+w):
                if (frame[row][col][0] < bandanaBGR[0]+approxFactor and frame[row][col][0] > bandanaBGR[0]-approxFactor) and (frame[row][col][1] < bandanaBGR[1]+approxFactor and frame[row][col][1] > bandanaBGR[1]-approxFactor) and (frame[row][col][2] < bandanaBGR[2]+approxFactor and frame[row][col][2] > bandanaBGR[2]-approxFactor):
                    count += 1
        if count/(w*h*(aboveFaceFactor-belowTopOfFaceFactor)) > matchThreashold:
            cv2.putText(frame, 'Zombie', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 3, cv2.LINE_AA)

            if (y+int(h/2))+int(cap.get(4)*scalingFactor*bodyShotFactor) < cap.get(4)*scalingFactor:
                ZombieLocation = [x+int(w/2),int(cap.get(4)/2)]
                frame[(y+int(h/2))+int(cap.get(4)*scalingFactor*bodyShotFactor)][x+int(w/2)] = [0,0,0] #should improve bodyshot by scaling it by size of face

    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
