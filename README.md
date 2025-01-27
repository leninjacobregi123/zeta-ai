Summarization Tool using Llama3.2

This Python script reads a transcription file, extracts the text, and generates a summary using an AI model. The summary is based on the context of the given transcription content, and the response is generated from a local API service.

## Features

- Reads transcription data from a JSON file.
- Sends the transcription data to a local API to generate a summary.
- Handles streaming API responses and outputs updates.
- Error handling for common issues like file not found or decoding errors.

## Requirements

To run this script, make sure you have the following libraries installed:

- `requests`: To send HTTP requests to the local API.
- `json`: To handle JSON data.

Install dependencies with pip:

```bash
pip install requests
```

## How It Works

1. **Reading Transcription**: The script reads a JSON transcription file, extracts all the text segments, and joins them into one large string.
2. **Summarization**: The transcription is sent as a payload to a local API (`http://localhost:11434/api/generate`) that processes the request and returns a summary based on the context of the input text.
3. **Error Handling**: The script includes error handling to catch file errors, JSON errors, and HTTP request issues.
4. **Summary Handling**: The summary text is printed as it’s being processed via a stream.

## File Structure

```
summarization_tool/
│
├── summarization_script.py      # The main script
├── transcription_with_timestamps.json  # The transcription file (example)
└── README.md                   # This README file
```

## Usage

1. Prepare the transcription file in the JSON format with the necessary structure (a list of text segments).
2. Place the transcription file in the same directory as the script.
3. Run the script:

```bash
python summarization_script.py
```

## Example

If you have a transcription file named `transcription_with_timestamps.json`, the script will read the file, extract the text, send it to the summarization API, and print the summary.

## Functions

- **`make_api_call(payload)`**: Sends a POST request to the local API and returns the full response text.
- **`generate_summary(text)`**: Creates a prompt using the input text and calls the `make_api_call` function to generate a summary.
- **`handle_summary_stream(response_text)`**: Handles and prints summary updates.
- **`read_transcription_from_file(transcription_file)`**: Reads the transcription file and returns the extracted text.
- **`main()`**: The main function that combines all the steps of reading the transcription and generating the summary.

## Error Handling

- **File Not Found**: If the transcription file is not found, an error message is displayed.
- **JSON Decode Error**: If the transcription file is not in valid JSON format, an error is displayed.
- **API Request Error**: If there is an issue with the API request, an error message is displayed.

## Notes

- Ensure the local API service at `http://localhost:11434/api/generate` is up and running for the script to work correctly.
- The script generates summaries ranging from 600 to 1000 words without special characters.

---

You can adjust or add any additional sections depending on your specific requirements or additional features.
