import cv2
import numpy as np
#Facial recognition with bandana to find Zombies

#find the center of the largest each rectangle and use that to find velocity. You have to account for motion
# of the platform as well though so this may not be possible

#Camera setup
cap = cv2.VideoCapture(0)
#hog = cv2.HOGDescriptor()
#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

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

minConfidence = 0 #1.5 should be good

# (80,150,0), (170,255,255) is a good blue range for the color mask
LowerMaskThreashold = 10
UpperMaskThreashold = 100

while(True):
    ret, image = cap.read()
    image = cv2.resize(image,(0,0), fx=0.5, fy=0.5)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    frameCenter = (int(image.shape[1]/2), int(image.shape[0]/2))            # You should hard code this as a variable for the specific camera
    #body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    torso_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')            # Also have a upper body detector for confidence

    upper_body = torso_cascade.detectMultiScale(gray, 1.1, 8)
    for (x, y, w, h) in upper_body:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cropped_image = image[y:y+h, x:x+w]
        hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (80,150,0), (170,255,255)) # Takes HSV color
        #cv2.imshow('mask red color', mask)
        if int(np.sum(mask == 255)/(w*h)*1000) > LowerMaskThreashold and int(np.sum(mask == 255)/(w*h)*1000) < UpperMaskThreashold:
            cv2.putText(image, 'Zombie', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,0), 3, cv2.LINE_AA)

    #full_body = body_cascade.detectMultiScale(gray, 1.1, 5)
    #for (x, y, w, h) in full_body:
        #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)


    cv2.imshow('Frame',image)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()





'''
while True:
    # Camera setup
    ret, frame = cap.read()
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
'''





'''
Full body Hog detector doesn't work that well.
(humans, confidence) = hog.detectMultiScale(image,
                                        winStride=(6, 6),
                                        padding=(8, 8),
                                        scale=1.2)


# Creates a list of humans in frame and sorts by size
     for entry in confidence:
         pass
         #print(entry)
     realHumans = []
     if len(humans) > 0:
         for i in range(len(confidence)):
             if confidence[i] > minConfidence:
                 realHumans.append([humans[i][0], humans[i][1], humans[i][2], humans[i][3]])
         realHumans = sorted(realHumans, key=lambda x:x[2]*x[3], reverse=True)

         if len(realHumans) > 0:
             humanCenter = (realHumans[0][0]+int(realHumans[0][2]/2),realHumans[0][1]+int(realHumans[0][3]/2))
             if not (humanCenter[0] < 0 or humanCenter[0] > image.shape[1] or humanCenter[1] < 0 or humanCenter[1] > image.shape[0]):
                 # Draws line from middle of screen to middle of person
                 cv2.line(image, humanCenter, frameCenter, (0, 255, 0), 3)

     for (x, y, w, h) in humans:
             cv2.rectangle(image,
                          (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

'''
