---

# ZETA AI

## Project Overview
This project provides a complete pipeline for downloading YouTube videos as audio, transcribing the audio using OpenAI's Whisper model, summarizing the transcription, generating flashcards, and organizing the content using RAG (Retrieval-Augmented Generation) via Milvus and Ollama. The solution integrates various functionalities like audio extraction, transcription, summarization, and machine learning-based search to enhance the accessibility and usability of video content.

### Features
1. **Audio Download**: Download YouTube videos as audio files and convert them into WAV format.
2. **Audio Transcription**: Use OpenAI's Whisper model to transcribe the audio and generate YouTube-style timestamps for each transcribed segment.
3. **Summarization**: Automatically summarize the transcribed text into a concise form using a summarization API.
4. **Flashcard Generation**: Convert the transcription and summary into flashcards with questions and answers.
5. **RAG Integration**: Use the Milvus vector database and Ollama for retrieval-augmented generation (RAG) to answer user queries from the transcription context.

---

## Requirements

Before running the code, make sure you have the following installed:

### Python Packages
The project requires the following Python libraries:
- `yt-dlp`: For downloading YouTube videos.
- `whisper`: OpenAI's Whisper model for transcription.
- `requests`: To make HTTP requests for summarization and flashcard generation.
- `json`: For handling JSON data.
- `pymilvus`: For connecting to and interacting with the Milvus vector database.
- `tqdm`: For progress bars during long-running operations.
- `torch`: PyTorch library for running machine learning models (required for Whisper).
- `ollama`: Ollama's API for embedding and chat-based interactions.

To install all necessary libraries, you can create a `requirements.txt` file with the following content:

```text
yt-dlp
whisper
requests
pymilvus
tqdm
torch
ollama
```

You can install them using pip:

```bash
pip install -r requirements.txt
```

### External Software
1. **FFmpeg**: The code uses FFmpeg for audio extraction and conversion (e.g., converting audio to WAV format). You can install FFmpeg on your system:
    - **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html).
    - **Linux**: Run `sudo apt install ffmpeg` (for Debian-based distros).
    - **MacOS**: Run `brew install ffmpeg` using Homebrew.

2. **Milvus Database**: Milvus is used for storing and searching embeddings. You need to set up a Milvus server. You can follow the official Milvus installation guide for your operating system: [Milvus Installation Guide](https://milvus.io/docs/install_standalone-docker.md).

3. **Ollama API**: For embedding and chat-based interactions, you need access to the Ollama API. You can sign up and get your access key on their official website: [Ollama](https://ollama.com/).

### Hardware Requirements
- **GPU** (Optional but recommended): If you want to speed up transcription using the Whisper model, having a GPU (CUDA-enabled) will significantly improve the performance.
- **Storage**: Depending on the length of the audio and transcription, ensure you have sufficient storage for the audio files, embeddings, and Milvus database.

---

## Setup Instructions

### Step 1: Install Python Dependencies
Clone the repository and install the required Python dependencies:

```bash
git clone https://github.com/your-repository-name.git
cd your-repository-name
pip install -r requirements.txt
```

### Step 2: Download FFmpeg
Make sure you have FFmpeg installed. You can verify this by running:

```bash
ffmpeg -version
```

If you don’t have FFmpeg installed, please follow the installation steps mentioned above.

### Step 3: Set Up Milvus
1. Download and install Milvus.
2. Start the Milvus server:
   - You can use Docker to run Milvus:
     ```bash
     docker run -d --name milvus_cpu -p 19530:19530 -v /var/lib/milvus --restart always milvusdb/milvus:latest
     ```
   - Alternatively, follow the Milvus installation guide for your OS to set it up manually.

3. Once Milvus is set up, you can proceed with using the script to insert data into Milvus.

### Step 4: Ollama API Setup
Make sure you have access to the Ollama API for generating embeddings and chat-based interactions. The code uses the Ollama API to generate both embeddings for text and responses for questions related to the transcription.

### Step 5: Prepare Your Input
You can use any YouTube video URL for transcription. The script will download the audio, convert it to WAV format, and then process it for transcription. Make sure the video URL is valid when prompted in the script.

---

## Usage

### 1. Download Audio and Transcribe
To start the process of downloading a YouTube video as an audio file and transcribing it, run the `download_audio.py` script:

```bash
python download_audio.py
```

It will prompt you to enter a YouTube video URL. The audio will be saved in the `output_audio.wav` file.

### 2. Transcribe and Generate Timestamps
After downloading the audio, you can run the transcription script to generate transcriptions with timestamps. The script will use the Whisper model to transcribe the audio file and save the transcription to a `transcription_with_timestamps.json` file.

```bash
python transcribe_audio.py
```

### 3. Summarize the Transcription
Once the transcription is ready, you can generate a summary using the `summarize_transcription.py` script:

```bash
python summarize_transcription.py
```

It will generate a summary of the transcribed text and print it to the console.

### 4. Generate Flashcards
You can generate flashcards from the transcription and its summary using the `generate_flashcards.py` script:

```bash
python generate_flashcards.py
```

It will print out a set of 20 flashcards, each with a question and an answer.

### 5. Retrieval-Augmented Generation (RAG) with Milvus
The project also implements Retrieval-Augmented Generation (RAG) using Milvus. After the embeddings are generated for the transcription, you can interact with the assistant by querying the Milvus database. The assistant will retrieve relevant snippets from the transcription and answer your questions.

To interact with the assistant, run the following:

```bash
python rag_query.py
```

It will prompt you to enter your query. The assistant will retrieve relevant snippets from the transcription and answer your question based on the context.

---


## Troubleshooting

### 1. FFmpeg Issues
- If you encounter errors related to FFmpeg, ensure that it is installed and added to your system's PATH.
- Make sure the `FFmpeg` binary is executable by running `ffmpeg -version`.

### 2. Milvus Connection Issues
- Ensure that the Milvus server is running and accessible at `localhost:19530`.
- If you're running Milvus in Docker, make sure the port mappings are correct.

### 3. API Errors
- If the Ollama API is returning errors, check your API key and ensure you have an active subscription with Ollama.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Conclusion
This project provides a full pipeline for downloading, transcribing, summarizing, and querying YouTube videos. It leverages state-of-the-art models such as Whisper, Milvus, and Ollama to deliver a highly effective content analysis tool. With this setup, users can easily extract valuable insights from videos and convert them into flashcards or summaries.

---

Feel free to modify the README as per your specific requirements and the structure of your repository!
