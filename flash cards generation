import requests
import json

def make_api_call(payload):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
            full_text = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    response_data = json.loads(line)
                    full_text += response_data["response"]
            return full_text
    except requests.RequestException as e:
        print("Error:", e)
        return None

def generate_flashcards(text):
    prompt = ("""
    You are a Flashcard Generating AI. Based on the content provided, create 20 flashcards. 
    Each flashcard should have a Question and an Answer. Focus on extracting key points, facts, or concepts from the content.
    Return the flashcards in the format:
    Flashcard 1:
    Question: <Insert question here>
    Answer: <Insert answer here>

    Flashcard 2:
    Question: <Insert question here>
    Answer: <Insert answer here>

    Ensure the flashcards are concise and relevant to the content.
    Content:""" + str(text))
    
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
    }
    response_data = make_api_call(payload)
    return response_data

def handle_flashcards_output(response_text):
    print("Generated Flashcards:")
    print(response_text)

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

# Main function to combine transcription and flashcard generation
def main():
    # Input file for transcription
    transcription_file = "transcription_with_timestamps.json"

    # Read the transcription
    transcription_text = read_transcription_from_file(transcription_file)

    if transcription_text:
        print("Generating flashcards...")
        # Generate the flashcards
        flashcards_result = generate_flashcards(transcription_text)
        handle_flashcards_output(flashcards_result)
    else:
        print("No transcription text to generate flashcards.")

if __name__ == "__main__":
    main()
