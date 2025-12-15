from flask import Flask, request, jsonify, render_template, redirect, url_for
import cv2
import mediapipe as mp
import os
from collections import Counter
import math

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Allow up to 100MB uploads

# Initialize MediaPipe models
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Helper function to calculate angle
def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c.y - b.y, c.x - b.x) -
                       math.atan2(a.y - b.y, a.x - b.x))
    return abs(ang)

# Analyze video frames
def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    predictions = []
    frame_count = 0

    if not cap.isOpened():
        print("[ERROR] Could not open video file")
        return {
            "event": "Error reading video",
            "risk": "Unknown",
            "precaution": "Check file format and try again"
        }

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        condition = None

        # Pose detection
        pose_results = pose.process(rgb)
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP].y
            shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            nose_y = landmarks[mp_pose.PoseLandmark.NOSE].y

            if hip_y < shoulder_y and nose_y > shoulder_y:
                condition = {
                    "event": "⚠️ Falling backward",
                    "risk": "High risk of head/back injury",
                    "precaution": "Check consciousness, support head/neck, call medical help"
                }
            elif hip_y < shoulder_y and nose_y < shoulder_y:
                condition = {
                    "event": "⚠️ Falling forward",
                    "risk": "Risk of facial injury or broken arms",
                    "precaution": "Ensure airway clear, stop bleeding, seek medical evaluation"
                }

            angle = get_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            )
            if angle < 120:
                condition = {
                    "event": "⚠️ Falling down",
                    "risk": "Possible fracture or trauma",
                    "precaution": "Do not move patient, call emergency services"
                }

        # Face detection
        face_results = face_mesh.process(rgb)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                top_lip = face_landmarks.landmark[13].y
                bottom_lip = face_landmarks.landmark[14].y
                mouth_open = abs(bottom_lip - top_lip)

                if mouth_open > 0.03:
                    condition = {
                        "event": "😡 Distress/anger detected",
                        "risk": "Emotional stress, possible breathing difficulty",
                        "precaution": "Calm patient, ensure safe environment, monitor breathing"
                    }

        if condition:
            predictions.append(condition)

    cap.release()
    print(f"[INFO] Processed {frame_count} frames from {video_path}")

    if predictions:
        most_common_event = Counter([p["event"] for p in predictions]).most_common(1)[0][0]
        final = next(p for p in predictions if p["event"] == most_common_event)
        print(f"[INFO] Final summarized prediction: {final}")
        return final
    else:
        return {
            "event": "No event detected",
            "risk": "No immediate health risk",
            "precaution": "Continue monitoring"
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        return redirect(url_for('upload'))
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print(f"[INFO] New user registered: {username}, Email: {email}")
    return redirect(url_for('upload'))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'video' not in request.files:
            print("[ERROR] No video file received in request")
            return jsonify({"error": "No video uploaded"}), 400

        video = request.files['video']
        if video.filename == '':
            print("[ERROR] Empty filename")
            return jsonify({"error": "Empty filename"}), 400

        os.makedirs("uploads", exist_ok=True)
        video_path = os.path.join("uploads", video.filename)
        video.save(video_path)
        print(f"[INFO] Video saved to {video_path}")

        if not os.path.exists(video_path):
            print("[ERROR] File not found after saving")
            return jsonify({"error": "File save failed"}), 500

        if os.path.getsize(video_path) == 0:
            print("[ERROR] Saved file is empty")
            return jsonify({"error": "Uploaded file is empty"}), 400

        prediction = analyze_video(video_path)
        print(f"[INFO] Prediction generated: {prediction}")
        return jsonify(prediction)

    except Exception as e:
        print(f"[ERROR] Exception in /predict: {type(e).__name__}: {e}")
        return jsonify({"error": f"Server error: {type(e).__name__}: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
