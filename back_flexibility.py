import cv2
import mediapipe as mp
import math

import numpy as np

def angle_between_points(p1, p2, p3):
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)

    ab = b - a
    ac = c - a

    cos_angle = np.dot(ab, ac) / (np.linalg.norm(ab) * np.linalg.norm(ac))
    angle = np.arccos(cos_angle)
    
    return np.degrees(angle)

angle = 0.0

# List to store angles for averaging
angles = []
max_angles_to_store = 30  # Maximum number of angles to store for averaging


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process the frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    h, w = image.shape[:2]


    # Draw landmarks
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Calculate midpoints only if landmarks are detected
        midpoint1 = (
            (int(results.pose_landmarks.landmark[11].x * w) + int(results.pose_landmarks.landmark[12].x * w)) // 2,
            (int(results.pose_landmarks.landmark[11].y * h) + int(results.pose_landmarks.landmark[12].y * h)) // 2)

        midpoint2 = (
            (int(results.pose_landmarks.landmark[23].x * w) + int(results.pose_landmarks.landmark[24].x * w)) // 2,
            (int(results.pose_landmarks.landmark[23].y * h) + int(results.pose_landmarks.landmark[24].y * h)) // 2)

        # Draw a line between the two midpoints
        cv2.line(frame, midpoint1, midpoint2, (0, 255, 0), 9)

                # Calculate midpoints only if landmarks are detected
        midpoint3 = (
            (int(results.pose_landmarks.landmark[27].x * w) + int(results.pose_landmarks.landmark[28].x * w)) // 2,
            (int(results.pose_landmarks.landmark[27].y * h) + int(results.pose_landmarks.landmark[28].y * h)) // 2)

        # Draw a line between the two midpoints
        cv2.line(frame, midpoint1, midpoint2, (0, 255, 0), 9)
        cv2.line(frame, midpoint2, midpoint3, (100, 0, 200), 9)

        angle = angle_between_points(midpoint1, midpoint2, midpoint3)

         # Store the angle for averaging
        angles.append(angle)
        if len(angles) > max_angles_to_store:  # Limit the number of stored angles
            angles.pop(0)  # Remove the oldest angle

        # Calculate the average angle
        average_angle = sum(angles) / len(angles)

        cv2.putText(frame, f'ang:{int(average_angle)}',
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        

    cv2.imshow('Pose Detection', frame)
    if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
