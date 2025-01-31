import yt_dlp

def download_audio(video_url, output_filename="output_audio.wav"):
    """
    Downloads the audio of a YouTube video and saves it in WAV format.
    
    Args:
        video_url (str): The URL of the YouTube video.
        output_filename (str): The name of the output file (default: output_audio.wav).
    """
    options = {
        'format': 'bestaudio/best',  # Select the best audio quality
        'extractaudio': True,        # Extract audio only
        'audioformat': 'wav',        # Convert audio to WAV format
        'outtmpl': output_filename,  # Save file with the given filename
        'postprocessors': [{         # Post-processing settings
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'postprocessor_args': [
            '-ar', '48000',  # Set sample rate to 48kHz
            '-ac', '2'       # Set channels to stereo
        ]
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            print(f"Downloading audio from: {video_url}")
            ydl.download([video_url])
            print(f"Audio successfully downloaded and saved as {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("YouTube Audio Downloader")
    video_url = input("Enter the YouTube video URL: ").strip()
    output_filename = "output_audio.wav"
    download_audio(video_url, output_filename)
