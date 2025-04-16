import whisper
from feedback import generate_interview_feedback

# Load the Whisper model (use "base" or "small" for faster performance)
model = whisper.load_model("base")

# Path to your interview audio or video file (can be .mp3, .wav, .mp4, .m4a, etc.)
input_file = "Guy.mp3"  # replace with the actual file you want to transcribe

# Transcribe the file
result = model.transcribe(input_file)

# Print the transcript for debugging purposes
print("\n🔊 TRANSCRIPT:\n")
print(result["text"])

# Optional: Save to file (for passing to the feedback generator)
with open("transcript.txt", "w") as f:
    f.write(result["text"])

# Generate feedback from the transcript and save it to feedback.json (JSON format)
generate_interview_feedback("transcript.txt", feedback_file="feedback.json")
