# import the necessary packages
import numpy as np
import face_recognition as fr
import cv2


video_capture = cv2.VideoCapture(0)

#Train the bot here 
Simon_image = fr.load_image_file("Simon.jpg")
Simon_face_encoding = fr.face_encodings(Simon_image)[0]

yorgo_image = fr.load_image_file("Yorgo.jpg")
yorgo_face_encoding = fr.face_encodings(yorgo_image)[0]

known_face_encondings = [Simon_face_encoding, yorgo_face_encoding]
known_face_names = ["Simon", "Yorgo"]

#Create the Frame
while True: 
    ret, frame = video_capture.read()

    rgb_frame = frame[:, :, ::-1]

    face_locations = fr.face_locations(rgb_frame)
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    #Face Comparison
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_face_encondings, face_encoding)
        
        #if face not recognized
        name = "Unknown"
    
        face_distances = fr.face_distance(known_face_encondings, face_encoding)

        best_match_index = np.argmin(face_distances)
    
        #if face recognized
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            import detect_drowsiness
 
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    #Show the frame
    cv2.imshow('Webcam_facerecognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()