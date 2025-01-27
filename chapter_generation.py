import json
from pymilvus import MilvusClient
import ollama
from tqdm import tqdm

def retrieve_data_from_db(milvus_client, collection_name):
    """
    Retrieve text data from the Milvus database.
    """
    print("Retrieving data from the database...")
    try:
        results = milvus_client.query(
            collection_name=collection_name,
            filter="id >= 0",  # Retrieve all records (changed 'expr' to 'filter')
            output_fields=["text"],  # Only retrieving the 'text' field
        )
        print(f"Retrieved {len(results)} records from the database.")
        return [result["text"] for result in results]
    except Exception as e:
        print(f"Error retrieving data from the database: {e}")
        return []

def generate_chapters_from_data(text_data, max_chapters=20):
    """
    Generate up to 'max_chapters' chapters from the text data.
    """
    print(f"Generating up to {max_chapters} chapters from the text data...")
    chapters = []
    chapter_size = len(text_data) // max_chapters  # Divide text into roughly equal chapters
    
    for i in range(max_chapters):
        start = i * chapter_size
        end = start + chapter_size
        if i == max_chapters - 1:  # Ensure the last chapter includes any remaining data
            end = len(text_data)
        chapter = " ".join(text_data[start:end])
        chapters.append(chapter)
        print(f"Chapter {i + 1}: {len(chapter)} characters")

    return chapters

def main():
    # Load transcription with timestamps
    output_file = "transcription_with_timestamps.json"
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            transcription = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{output_file}' not found. Please ensure the file exists.")
        return
    
    # Initialize Milvus client
    milvus_client = MilvusClient(uri="./milvus_demo.db")
    collection_name = "my_rag_collection"
    
    # Retrieve text data from the database
    text_data = retrieve_data_from_db(milvus_client, collection_name)
    
    if not text_data:
        print("No data found in the collection. Exiting.")
        return

    # Generate chapters
    chapters = generate_chapters_from_data(text_data, max_chapters=20)

    # Display chapters
    for i, chapter in enumerate(chapters):
        print(f"\n--- Chapter {i + 1} ---\n")
        print(chapter[:500])  # Display the first 500 characters of each chapter

    # Optionally save chapters to a file
    output_file = "generated_chapters.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(chapters, file, indent=4, ensure_ascii=False)
    print(f"\nChapters saved successfully to '{output_file}'.")

if __name__ == "__main__":
    main()
