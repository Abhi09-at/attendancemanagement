from flask import Flask, render_template, Response
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

app = Flask(__name__)

# Path to the directory containing training images
path = r"C:\Users\vishr\mini\Training_images"  # Update this to the correct folder path
images = []
classNames = []

# Load valid image files from the directory
valid_extensions = ('.jpg', '.jpeg', '.png')  # Add more extensions if needed
myList = [file for file in os.listdir(path) if file.lower().endswith(valid_extensions)]
print("Valid Images Found:", myList)

for cl in myList:
    curImg = cv2.imread(os.path.join(path, cl))
    if curImg is not None:  # Check if the image was loaded successfully
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])  # Extract the name without the file extension
    else:
        print(f"Warning: Could not load image {cl}")
print("Class Names:", classNames)

# Function to encode all images
def findEncodings(images):
    encodeList = []
    for i, img in enumerate(images):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]  # Get the first encoding
            encodeList.append(encode)
        except IndexError:
            print(f"Warning: No face detected in image '{classNames[i]}'. Skipping.")
    return encodeList

# Function to mark attendance
def markAttendance(name):
    try:
        with open('Attendance.csv', 'a+') as f:  # Open in append mode
            f.seek(0)  # Move to the beginning of the file
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]

            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%Y-%m-%d %H:%M:%S')  # Include date and time
                f.writelines(f'{name},{dtString}\n')
    except Exception as e:
        print(f"Error marking attendance: {e}")

# Encode known images
print("Encoding images...")
encodeListKnown = findEncodings(images)
print("Encoding Complete")

# Flask Route for rendering the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Video Streaming Generator
def gen_frames():
    cap = cv2.VideoCapture(0)  # Open the webcam
    while True:
        success, img = cap.read()
        if not success:
            break

        # Resize frame for faster processing
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Detect faces and encode them in the current frame
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        # Match detected faces with known encodings
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            # Find the best match with a threshold
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex] and faceDis[matchIndex] < 0.5:  # Adjust threshold if needed
                name = classNames[matchIndex].upper()
                print(f"Detected: {name}")
                markAttendance(name)
            else:
                name = "Unknown"
                print("Detected: Unknown")

            # Draw bounding box and name on the image
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)  # Green for known, Red for unknown
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Encode the image as JPEG and yield it to be streamed to the HTML page
        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask Route for video streaming
@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
