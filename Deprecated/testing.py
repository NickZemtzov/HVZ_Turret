#Based on good tutorial: https://www.youtube.com/playlist?list=PLzMcBGfZo4-lUA8uGjeXhBUUzPYc6vZRn

import cv2
import numpy as np
import imutils

'''
#Basic Manipulation
img = cv2.imread('ZemtzovPhoto.jpg',0)
# 0 as the second parameter makes this grayscale
img = cv2.resize(img,(400,400))
#to resize by a fraction: resize(img,(0,0), fx=0.5, fy=0.5)
img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite('newPhoto.jpg',img)

#to open the image in a window
cv2.imshow('Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
#Facial recognition original
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)

        roi_gray = gray[y:y+h,x:x+w]
        roi_color = frame[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray,1.3,5)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),5)


    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

'''
#Body recognition
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 3)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)

    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''

'''
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
#out = cv2.VideoWriter(
#    'output.avi',
#    cv2.VideoWriter_fourcc(*'MJPG'),
#    15.,
#    (640,480))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)

    # Write the output video
    #out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
#out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)
'''

def hog():
    cv2.startWindowThread()

# open webcam video stream
    cap = cv2.VideoCapture(0)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    while(True):
        # Capture frame-by-frame
        ret, image = cap.read()


# Resizing the Image
        image = cv2.resize(image,(0,0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Detecting all humans
        (humans, _) = hog.detectMultiScale(image,
                                            winStride=(6, 6),
                                            padding=(8, 8),
                                            scale=1.21)
# getting no. of human detected
        print('Human Detected : ', len(humans))

# Drawing the rectangle regions
        for (x, y, w, h) in humans:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

# Displaying the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
    cap.release()
# and release the output
#out.release()
# finally, close the window
    cv2.destroyAllWindows()
    cv2.waitKey(1)


def haar(cascade):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade)

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame,(0,0), fx=0.5, fy=0.5)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.05, 3)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),5)

        cv2.imshow('Frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



#hog()
#haar('haarcascade_fullbody.xml')# - not quite as good as the hog with padding but may do the job and be better cuz it's faster
#haar('haarcascade_frontalface_default.xml')
#haar('haarcascade_upperbody.xml')

