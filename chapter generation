import json
from pymilvus import MilvusClient
import ollama
from tqdm import tqdm
import os

def emb_text(text):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

def main():
    output_file = "transcription_with_timestamps.json"
    embedding_file = "embeddings_cache.json"

    # Load the transcription JSON
    with open(output_file, "r", encoding="utf-8") as file:
        transcription = json.load(file)

    # Initialize Milvus client
    milvus_client = MilvusClient(uri="./milvus_demo.db")
    collection_name = "my_rag_collection"

    # Create collection if it does not exist
    if milvus_client.has_collection(collection_name):
        print("Collection already exists. Skipping creation.")
    else:
        embedding_dim = len(emb_text("This is a test"))
        milvus_client.create_collection(
            collection_name=collection_name,
            dimension=embedding_dim,
            metric_type="IP",
            consistency_level="Strong",
        )
        print("Collection created successfully.")

    # Load or generate embeddings
    if os.path.exists(embedding_file):
        with open(embedding_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Loaded embeddings from cache.")
    else:
        data = []
        for i, entry in enumerate(tqdm(transcription, desc="Creating embeddings")):
            text = entry["text"]
            embedding = emb_text(text)
            data.append({"id": i, "vector": embedding, "text": text})
        with open(embedding_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("All embeddings created and saved to cache successfully.")

    # Insert data into Milvus
    milvus_client.insert(collection_name=collection_name, data=data)
    print("RAG data updated successfully.")

    # System prompt for chapter generation
    SYSTEM_PROMPT = """
    You are an AI assistant. Your task is to organize the provided transcripts into meaningful flashcards . Each section of the tutorial must correspond to a single chapter, with a specific and descriptive heading. Use the format 'Chapter 1: [Heading]'. Group related content under the appropriate chapter and maintain chronological order.
    """

    # Combine all text from transcription
    all_text = "\n".join([f"{entry['timestamp']} {entry['text']}" for entry in transcription])

    # User prompt to generate chapters
    USER_PROMPT = f"""
    Organize the following transcript text into meaningful s:
    <context>
    {all_text}
    </context>
    """

    # Call Ollama's chat model for chapter generation
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT},
        ],
    )

    # Extract and print the generated chapters
    print("Generated chapters from transcription:")
    chapters = response["message"]["content"]
    print(chapters)

    # System prompt for flashcard creation
    FLASHCARD_PROMPT = """
    You are an AI assistant. Your task is to create 20 concise flashcards based on the provided transcription and its summary. Each flashcard should have a 'Question' and an 'Answer'. Ensure the content covers key points and concepts effectively.
    """

    # User prompt for flashcards
    USER_PROMPT_FLASHCARDS = f"""
    Create 20 flashcards from the following transcription and summary:
    <context>
    {all_text}\n\n{chapters}
    </context>
    """

    # Call Ollama's chat model for flashcard generation
    flashcards_response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": FLASHCARD_PROMPT},
            {"role": "user", "content": USER_PROMPT_FLASHCARDS},
        ],
    )

    # Extract and print the generated flashcards
    print("Generated flashcards:")
    print(flashcards_response["message"]["content"])

if __name__ == "__main__":
    main()
