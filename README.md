Patient Safety AI – Real‑Time Monitoring & Alerts
📖 Overview
Patient Safety AI is an intelligent healthcare monitoring platform that uses computer vision and real‑time alerts to enhance patient safety. Built with Flask, MediaPipe, and Twilio, the system analyzes patient activity videos to detect falls, distress, or unusual behavior, and instantly notifies staff via SMS and dashboard alerts.
This project is designed for hospitals, clinics, and caregivers to respond quickly to emergencies, reduce risks of injury, and ensure continuous patient monitoring.

✨ Features
- 📹 Video Uploads: Securely upload patient activity recordings for automated analysis.
- ⚠️ Risk Detection: Detect falls, distress, or unusual behavior using pose estimation and facial landmark tracking.
- 📲 Instant Alerts: Notify healthcare staff immediately via SMS and dashboard messages when risks are detected.
- 🔒 Reliability & Security: Scalable backend architecture, safe credential handling, and professional UI.

🛠️ Tech Stack
- Backend: Flask (Python)
- Frontend: HTML, CSS, Bootstrap, JavaScript
- AI Models: MediaPipe Pose & FaceMesh
- Notifications: Twilio SMS API
- Other Tools: OpenCV for video processing

🚀 Getting Started
1. Clone the repository
git clone https://github.com/your-username/patient-safety-ai.git
cd patient-safety-ai


2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


3. Install dependencies
pip install -r requirements.txt


4. Set environment variables
Create a .env file in the project root:
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_phone_number
STAFF_PHONE=recipient_staff_number


⚠️ Important: Never commit .env to GitHub. Add it to .gitignore.
5. Run the app
python app.py


Visit http://127.0.0.1:5000 in your browser.

📂 Project Structure
patient-safety-ai/
│
├── app.py                # Flask backend
├── templates/            # HTML templates (login, signup, upload, index)
├── static/               # CSS, JS, assets
├── uploads/              # Uploaded video files
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation



📸 Screenshots
- Login Page – Secure access for staff
- Signup Page – Register new users
- Upload Page – Upload patient activity videos
- Dashboard Alerts – Real‑time risk detection and notifications

⚠️ Security Notes
- Do not hardcode Twilio credentials in your code. Use environment variables.
- Revoke any exposed tokens immediately in the Twilio Console.
- Always add .env to .gitignore before pushing to GitHub.

👩‍💻 Author
Developed by Mamatha Pamarthi
B.Tech in Computer Science & Engineering (AI & Data Science)
Passionate about AI, healthcare innovation, and building secure, scalable web platforms.
