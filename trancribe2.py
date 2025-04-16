import ffmpeg
import whisper
from feedback import generate_interview_feedback

def extract_audio_from_video(video_path, audio_path):
    ffmpeg.input(video_path).output(audio_path).run()

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# File paths
video_path = 'interview.mp4'
audio_path = 'audio_from_video.wav'
transcript_file = 'transcript.txt'
feedback_file = 'feedback.json'

# Extract audio
extract_audio_from_video(video_path, audio_path)

# Transcribe audio
transcribed_text = transcribe_audio(audio_path)

# Save transcript to file
with open(transcript_file, 'w', encoding='utf-8') as f:
    f.write(transcribed_text)

print("✅ Transcript saved to transcript.txt")
print("Transcribed Text:")
print(transcribed_text)

# Generate structured feedback and save it as JSON
generate_interview_feedback(transcript_file, feedback_file)
