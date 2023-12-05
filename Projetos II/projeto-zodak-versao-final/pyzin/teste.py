
import face_recognition
import cv2
import numpy as np
import json

# Get a reference to webcam #0 (the default one)

video = cv2.VideoCapture()

ip = "https://192.168.1.4:8080/video"
# video.open(ip)


RES = 1 # 1 to 10
video_capture =   cv2.VideoCapture(0) #  video

# Load a sample picture and learn how to recognize it.
benjamin_image = face_recognition.load_image_file("images/benjamin.jpg")

benjamin_face_encoding = face_recognition.face_encodings(benjamin_image)[0]

# Load a second sample picture and learn how to recognize it.
kellen_image = face_recognition.load_image_file("images/kellen.jpg")
kellen_face_encoding = face_recognition.face_encodings(kellen_image)[0]


# Load a second sample picture and learn how to recognize it.
vitor_image = face_recognition.load_image_file("images/vitor.jpg")
vitor_face_encoding = face_recognition.face_encodings(vitor_image)[0]

gabriel_image = face_recognition.load_image_file("images/gabriel.jpg")
gabriel_face_encoding = face_recognition.face_encodings(gabriel_image)[0]



# Create arrays of known face encodings and their names
known_face_encodings = [
    benjamin_face_encoding, kellen_face_encoding, vitor_face_encoding, gabriel_face_encoding
]

print(kellen_face_encoding)

known_face_names = [
    "Benjamin",
    "Kellen",
    "Bizinho",
    "viado"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []


process_this_frame = True
c= 0
while True:
    c+=1
    # Grab a single frame of video

    # Only process every other frame of video to save time

    ret, frame = video_capture.read()

    if c % 10 ==0:

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=(10/RES)/10, fy=(10/RES)/10)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55 )
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        
        top *= RES
        right *= RES
        bottom *= RES
        left *= RES

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()