from pydub import AudioSegment
import math
import os

# Load your interview file
audio = AudioSegment.from_file("Guy.mp3")

# Duration of each chunk (in milliseconds)
chunk_length_ms = 30 * 1000  # 30 seconds

# Total number of chunks
total_chunks = math.ceil(len(audio) / chunk_length_ms)

# Create output folder if not exists
output_dir = "chunks"
os.makedirs(output_dir, exist_ok=True)

print(f"Splitting into {total_chunks} chunks...")

for i in range(total_chunks):
    start = i * chunk_length_ms
    end = min((i + 1) * chunk_length_ms, len(audio))
    chunk = audio[start:end]
    chunk.export(f"{output_dir}/chunk_{i+1}.mp3", format="mp3")
    print(f"Saved chunk {i+1}")

print("✅ Done!")
