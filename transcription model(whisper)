import whisper
import os
import json
from datetime import timedelta
import torch

def format_timestamp(seconds):
    """
    Convert seconds to a YouTube-style timestamp (e.g., 0:01, 1:23).
    """
    return str(timedelta(seconds=int(seconds))).lstrip("0:").replace("0", "", 1) if seconds else "0:00"

def transcribe_audio_with_timestamps(audio_path, model_size="base"):
    """
    Transcribe audio using OpenAI Whisper and generate YouTube-style timestamps.

    Parameters:
        audio_path (str): Path to the audio file.
        model_size (str): The size of the Whisper model to use (e.g., "tiny", "base", "small", "medium", "large").

    Returns:
        List of dictionaries containing timestamps and text segments.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"The file {audio_path} does not exist.")

    # Check if GPU is available and use it if possible
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the Whisper model and move it to the appropriate device
    print(f"Loading Whisper model on {device}...")
    model = whisper.load_model(model_size).to(device)

    # Transcribe the audio
    print("Transcribing audio...")
    result = model.transcribe(audio_path, word_timestamps=True)

    # Process segments for YouTube-style timestamps
    segments = result.get("segments", [])
    transcription = []

    for segment in segments:
        start_time = format_timestamp(segment["start"])
        text = segment["text"].strip()
        transcription.append({"timestamp": start_time, "text": text})

    return transcription

def save_transcription_to_file(transcription, output_file):
    """
    Save the transcription with timestamps to a JSON file.

    Parameters:
        transcription (list): List of dictionaries containing timestamps and text.
        output_file (str): Path to the output JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(transcription, file, indent=4, ensure_ascii=False)
    print(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    # Input audio file
    audio_file = "output_audio.wav.wav"

    # Output file for transcription
    output_file = "transcription_with_timestamps.json"

    try:
        # Transcribe the audio file
        transcription = transcribe_audio_with_timestamps(audio_file, model_size="base")

        # Save the transcription to a file
        save_transcription_to_file(transcription, output_file)

        # Print the transcription
        for entry in transcription:
            print(f"[{entry['timestamp']}] {entry['text']}")

    except Exception as e:
        print(f"An error occurred: {e}")
