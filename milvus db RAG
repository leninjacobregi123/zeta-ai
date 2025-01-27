import json
from pymilvus import MilvusClient
import ollama
from tqdm import tqdm

def emb_text(text):
    """
    Generate embedding for the given text using the Ollama embeddings model.
    """
    response = ollama.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

def main():
    # Load transcription with timestamps
    output_file = "transcription_with_timestamps.json"
    
    with open(output_file, "r", encoding="utf-8") as file:
        transcription = json.load(file)
    
    # Get embedding dimension using a sample text
    embedding_dim = len(emb_text("This is a test"))
    print(f"Embedding dimension: {embedding_dim}")
    
    # Initialize Milvus client
    milvus_client = MilvusClient(uri="./milvus_demo.db")
    collection_name = "my_rag_collection"
    
    # Drop collection if it already exists
    if milvus_client.has_collection(collection_name):
        milvus_client.drop_collection(collection_name)
    
    # Create new collection
    milvus_client.create_collection(
        collection_name=collection_name,
        dimension=embedding_dim,
        metric_type="IP",
        consistency_level="Strong",
    )
    print("Collection created successfully.")
    
    # Prepare data for insertion into Milvus
    data = []
    for i, entry in enumerate(tqdm(transcription, desc="Creating embeddings")):
        text = entry["text"]
        timestamp = entry["timestamp"]
        embedding = emb_text(text)
        
        # Ensure embedding is valid
        if len(embedding) == embedding_dim:
            data.append({
                "id": i,
                "vector": embedding,
                "text": text,
                "timestamp": timestamp  # Include timestamp in data for RAG retrieval
            })
        else:
            print(f"Skipping entry {i} due to empty or malformed embedding")
    
    # Ensure the number of rows is correct
    if len(data) != len(transcription):
        print(f"Warning: Data length mismatch! {len(data)} embeddings were inserted out of {len(transcription)} total entries.")
    
    # Insert data into Milvus
    print("All embeddings created successfully.")
    print(f"Total embeddings: {len(data)}")
    
    if len(data) > 0:
        milvus_client.insert(collection_name=collection_name, data=data)
        print("RAG data updated successfully.")
    else:
        print("No valid embeddings to insert.")
    
    SYSTEM_PROMPT = """
    Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
    """
    
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Search the Milvus collection using the embedding of the user's query
        search_res = milvus_client.search(
            collection_name=collection_name,
            data=[emb_text(user_query)],
            limit=3,
            search_params={"metric_type": "IP", "params": {}},
            output_fields=["text", "timestamp"],  # Include timestamp in the search results
        )
        
        # Collect the retrieved text and timestamps from search results
        retrieved_lines = []
        timestamps = []
        for res in search_res[0]:  # Iterate over the first result (as we are limiting the search to 3)
            retrieved_lines.append(res["entity"]["text"])
            timestamps.append(res["entity"]["timestamp"])
        
        # Prepare context with timestamps
        context = "\n".join([f"[{timestamps[i]}] {retrieved_lines[i]}" for i in range(len(retrieved_lines))])
        
        # Format the user prompt for the assistant
        USER_PROMPT = f"""
        Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
        <context>
        {context}
        </context>
        <question>
        {user_query}
        </question>
        """
        
        # Query Ollama for the response
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
            ],
        )
        
        # Output the AI's response
        print("AI:", response["message"]["content"])

if __name__ == "__main__":
    main()
