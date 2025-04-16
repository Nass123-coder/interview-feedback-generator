from flask import Flask, request, jsonify
import whisper
from feedback import generate_interview_feedback
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_audio():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Transcribe
    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    # Save transcript
    transcript_file = "transcript.txt"
    with open(transcript_file, "w") as f:
        f.write(result["text"])

    # Generate feedback JSON
    feedback_file = "feedback.json"
    generate_interview_feedback(transcript_file, feedback_file)

    # Load the feedback JSON and return it
    with open(feedback_file, 'r') as f:
        feedback = json.load(f)

    return jsonify(feedback)

if __name__ == '__main__':
    app.run(debug=True)
