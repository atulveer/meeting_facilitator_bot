import face_recognition
import os
import cv2
import numpy as np

def rec_faces():
    known_face_encodings = []
    known_face_names = []

    video_capture = cv2.VideoCapture(0)

    for file in os.listdir('face_data'):
        entity_name = file.split('.')[0]
        entity_image = face_recognition.load_image_file("face_data/{}".format(file))
        entity_face_encoding = face_recognition.face_encodings(entity_image)[0]
        known_face_encodings.append(entity_face_encoding)
        known_face_names.append(entity_name)

    face_locations = []
    face_encodings = []
    face_names = []

    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    video_capture.release()
    cv2.destroyAllWindows()
    return face_names

if __name__ == '__main__':
    face_names = rec_faces()
    print(face_names)
