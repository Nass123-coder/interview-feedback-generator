from keras.models import load_model
import cv2
import numpy as np
import mediapipe as mp
import json

# Load emotion recognition model
def load_emotion_recognition_model():
    return load_model("fer2013_mini_XCEPTION.102-0.66.hdf5", compile=False)

# Load MediaPipe modules
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

# Face detector
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Preprocess face for emotion model
def preprocess(face_roi):
    face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (64, 64))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)
    return face

# Dummy analysis functions
def calculate_confidence_from_emotions(emotions):
    return float(np.max(emotions)) * 100

def analyze_emotion_patterns(timeline):
    return {"most_common_emotion": "happy"}  # Replace with actual logic if needed

def analyze_confidence_trends(confidences):
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    return {"average_confidence": round(avg_conf, 2)}

# Dummy gesture classification
def recognize_hand_gesture(landmarks):
    return "open_hand" if landmarks else "no_hand_detected"

# Dummy posture classification
def analyze_posture(landmarks):
    return "standing" if landmarks else "not_detected"

# Communication skills assessment
def communication_skills_assessment(emotions, gestures, postures):
    gesture_score = len(set(gestures)) / (len(gestures) + 1e-5) * 10  # Diversity of gestures
    posture_score = 10 if "standing" in postures else 5               # Standing = confident
    emotion_engagement = any("happy" in str(e) or "surprise" in str(e) for e in emotions)
    emotion_score = 10 if emotion_engagement else 5                   # Emotion presence = better delivery

    overall_score = (gesture_score + posture_score + emotion_score) / 3

    return {
        "gesture_score": round(gesture_score, 2),
        "posture_score": posture_score,
        "emotion_score": emotion_score,
        "overall_communication_score": round(overall_score, 2),
        "feedback": (
            "Great non-verbal communication." if overall_score > 7 else
            "Good start, but try to show more emotion or varied gestures."
        )
    }

# Main analyzer
def analyze_facial_expression(video):
    emotional_model = load_emotion_recognition_model()
    cap = cv2.VideoCapture(video)

    confidence_scores = []
    emotion_timeline = []
    gestures_detected = []
    postures_detected = []

    with mp_hands.Hands(static_image_mode=False, max_num_hands=2) as hands, \
         mp_pose.Pose(static_image_mode=False) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Face detection & emotion analysis
            faces = face_detector.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                face_roi = frame[y:y+h, x:x+w]
                emotions = emotional_model.predict(preprocess(face_roi))
                confidence_score = calculate_confidence_from_emotions(emotions)
                confidence_scores.append(confidence_score)
                emotion_timeline.append(emotions)

            # Gesture recognition
            hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            gesture = recognize_hand_gesture(hand_results.multi_hand_landmarks)
            gestures_detected.append(gesture)

            # Posture recognition
            pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            posture = analyze_posture(pose_results.pose_landmarks)
            postures_detected.append(posture)

    cap.release()

    # Prepare result
    result = {
        'emotion_analysis': analyze_emotion_patterns(emotion_timeline),
        'confidence_analysis': analyze_confidence_trends(confidence_scores),
        'gesture_summary': {
            'gestures': gestures_detected[:5],
            'sample': gestures_detected[:10]
        },
        'posture_summary': {
            'postures': postures_detected[:5],
            'sample': postures_detected[:10]
        },
        'communication_assessment': communication_skills_assessment(
            emotion_timeline, gestures_detected, postures_detected
        )
    }

    return json.dumps(result, indent=4)  # Return result as JSON string

# Run the analysis and return as JSON
video_path = r'C://Users//DELL//Videos//Captures//Title 2025-04-03 21-14-58.mp4'
json_response = analyze_facial_expression(video_path)
print(json_response)
