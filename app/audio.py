import os
import json
import tempfile
from pydub import AudioSegment
import speech_recognition as sr

def analyze_audio_communication(mp3_path):
    # Convert MP3 to WAV for processing
    try:
        audio = AudioSegment.from_file(mp3_path)
    except Exception as e:
        return {"error": f"Failed to read MP3 file: {str(e)}"}

    # Save as temporary WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        wav_path = tmp_wav.name
        audio.export(wav_path, format="wav")

    # Initialize speech recognizer
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = ""
    except Exception as e:
        text = ""
        print(f"Speech recognition failed: {e}")

    # Clean up temp WAV file
    os.remove(wav_path)

    # Compute stats
    words = text.split()
    word_count = len(words)
    duration_sec = len(audio) / 1000.0  # Convert ms to seconds
    speaking_rate_wpm = (word_count / duration_sec) * 60 if duration_sec > 0 else 0
    loudness_db = audio.dBFS

    result = {
        "speech_transcript_preview": text[:100] + ("..." if len(text) > 100 else ""),
        "word_count": word_count,
        "duration_seconds": round(duration_sec, 2),
        "speaking_rate_wpm": round(speaking_rate_wpm, 2),
        "average_loudness_dB": round(loudness_db, 2),
        "audio_score": 10 if speaking_rate_wpm > 90 and loudness_db > -20 else 6
    }

    return result

if __name__ == "__main__":
    # Replace this path with your MP3 file path
    mp3_file = r"C://Users//DELL//Music//DEEP HOUSE - INDIA//03._Status_Quo_SA_&_BusyExplore_-_Talk_To_Me_(Lofi_Deep).mp3"

    if not os.path.exists(mp3_file):
        print(json.dumps({"error": "MP3 file not found"}, indent=4))
    else:
        analysis = analyze_audio_communication(mp3_file)
        print(json.dumps(analysis, indent=4))
