import requests
import json

def make_api_call(payload):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        full_text = ""
        with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    response_data = json.loads(line)
                    full_text += response_data["response"]
        return full_text                    
    except requests.RequestException as e:
        print("Error:", e)
        return None

def generate_summary(text):
    prompt = ("""
    You are a Summarizing AI. You should summarize the given content.The summary should be minimum 600 words and it can go upto 1000 words.
    Find the context/Main Factor of the text and the summarize based on it.The response should not contain any special characters it must only include numbers and text.
    Content:""" + str(text))
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
    }
    response_data = make_api_call(payload)
    return response_data

def handle_summary_stream(response_text):
    print("Summary update:", response_text)

# Read the transcription file and extract text
def read_transcription_from_file(transcription_file):
    try:
        with open(transcription_file, "r", encoding="utf-8") as file:
            transcription_data = json.load(file)
        # Extract text from the transcription (combine all segments)
        full_text = " ".join([segment["text"] for segment in transcription_data])
        return full_text
    except FileNotFoundError:
        print(f"The file {transcription_file} was not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding the transcription file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main function to combine transcription and summarization
def main():
    # Input file for transcription
    transcription_file = "transcription_with_timestamps.json"

    # Read the transcription
    transcription_text = read_transcription_from_file(transcription_file)

    if transcription_text:
        print("Generating summary...")
        # Generate the summary
        summary_result = generate_summary(transcription_text)
        handle_summary_stream(summary_result)
    else:
        print("No transcription text to summarize.")

if __name__ == "__main__":
    main()
