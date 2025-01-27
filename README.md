---

# YouTube Audio Downloader

A Python script to download the audio from a YouTube video and save it in WAV format.

## Features

- Downloads the best audio quality available from a YouTube video.
- Converts the audio to WAV format.
- Allows custom file naming for the output file.
- Uses `yt-dlp` for downloading and `ffmpeg` for post-processing the audio.

## Requirements

To run this script, you'll need the following:

- Python 3.x
- `yt-dlp`: A command-line tool to download videos from YouTube and other sites.
- `ffmpeg`: A multimedia framework for processing video, audio, and other multimedia files.

### Installing Dependencies

1. Install Python 3.x from the official [Python website](https://www.python.org/downloads/).
2. Install `yt-dlp` by running the following command:

```bash
pip install yt-dlp
```

3. Install `ffmpeg` by following the instructions on the [FFmpeg official website](https://ffmpeg.org/download.html).

## Usage

1. Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/youtube-audio-downloader.git
```

2. Navigate to the project directory:

```bash
cd youtube-audio-downloader
```

3. Run the script:

```bash
python download_audio.py
```

4. Enter the YouTube video URL when prompted, and the audio will be downloaded and saved as `output_audio.wav`.

## Custom Output Filename

You can specify a custom output filename by modifying the `output_filename` parameter in the script.

```python
output_filename = "your_custom_filename.wav"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any of the sections above, such as the repository URL, the custom filename example, or other relevant details.


Whisper Audio Transcription with Timestamps

This project uses OpenAI's Whisper model to transcribe audio files and generate YouTube-style timestamps for each segment. The timestamps are saved in a JSON format and can be used for various purposes, such as creating subtitles or analyzing speech content.

Features

- Transcribes audio files using Whisper (OpenAI's speech-to-text model).
- Generates YouTube-style timestamps for each transcribed segment.
- Saves the transcription with timestamps in a JSON file.
- Supports different model sizes for Whisper, including `tiny`, `base`, `small`, `medium`, and `large`.

## Requirements

- Python 3.x
- PyTorch (with CUDA support if GPU is available)
- Whisper (OpenAI's Whisper library)

You can install the required dependencies using pip:

```bash
pip install torch whisper
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whisper-audio-transcription.git
   cd whisper-audio-transcription
   ```

2. Place your audio file in the same directory or specify the full path in the script.

3. Modify the script as needed:
   - Set the path to the audio file (`audio_file`).
   - Specify the desired output file name (`output_file`).

4. Run the script:
   ```bash
   python transcribe_audio.py
   ```

5. The transcription will be printed in the console, and the JSON file with timestamps will be saved to the specified output file.

## Functions

### `format_timestamp(seconds)`
Converts seconds to a YouTube-style timestamp (e.g., `0:01`, `1:23`).

### `transcribe_audio_with_timestamps(audio_path, model_size="base")`
Transcribes the audio file and generates YouTube-style timestamps.

- **Parameters**:
  - `audio_path` (str): Path to the audio file.
  - `model_size` (str): The size of the Whisper model to use. Options include `tiny`, `base`, `small`, `medium`, `large`.

- **Returns**: A list of dictionaries containing timestamps and transcribed text.

### `save_transcription_to_file(transcription, output_file)`
Saves the transcription with timestamps to a JSON file.

- **Parameters**:
  - `transcription` (list): List of dictionaries containing timestamps and text.
  - `output_file` (str): Path to the output JSON file.

## Example Output

The output is a JSON file containing transcriptions with timestamps:

```json
[
    {
        "timestamp": "0:00",
        "text": "Hello, welcome to this transcription example."
    },
    {
        "timestamp": "0:20",
        "text": "This is an example of audio transcribed with timestamps."
    }
]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Feel free to update this based on your actual repository URL and any additional details specific to your project!
