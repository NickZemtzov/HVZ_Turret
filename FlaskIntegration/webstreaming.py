from imutils.video import VideoStream
from flask import Response, Flask, render_template, request
import threading
import argparse
import datetime
import imutils
import time
import cv2
import serial
import os

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to warmup
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Arduino Communication
for i in range(3):
    try:
        os.system(f"sudo chmod a+rw /dev/ttyUSB{i}")
        arduino=serial.Serial(port=f'/dev/ttyUSB{i}', baudrate=115200, timeout=0.1)
    except Exception as e:
        pass
        #print(f"No Arduino Detected: {e}")

@app.route("/")
def index():
    global state
    text = request.args.get('button_text')
    if text == "Down": # Keypress w
        arduino.write(bytes("4",'utf-8'))
    elif text == "Up": #Keypress s
        arduino.write(bytes("5",'utf-8'))
    elif text == "Left": #Keypress a
        arduino.write(bytes("6",'utf-8'))
    elif text == "Stop Left": #Unpress a
        arduino.write(bytes("6",'utf-8'))
    elif text == "Right": #Keypress d
        arduino.write(bytes("7",'utf-8'))
    elif text == "Stop Right": #Unpress d
        arduino.write(bytes("7",'utf-8'))
    elif text == "Rev On": #Keypress l-shift
        arduino.write(bytes("3",'utf-8'))
    elif text == "Rev Off": #Unpress l-shift
        arduino.write(bytes("3",'utf-8'))
    elif text == "Reload": #Keypress r
        arduino.write(bytes("0",'utf-8'))
    print(text)
    return render_template("index_full.html")

def detection():
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock
    
    # loop over frames from the video stream
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=800)
		with lock:
			outputFrame = frame.copy()


def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	t = threading.Thread(target=detection)
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host='0.0.0.0', port=8000, debug=True,
    		threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()




