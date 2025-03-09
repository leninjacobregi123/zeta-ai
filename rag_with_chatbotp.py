from glob import glob
import ollama
from pymilvus import MilvusClient
from tqdm import tqdm
import json
import os
import PyPDF2  
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage  


os.environ["CUDA_VISIBLE_DEVICES"] = "0" 

class RAGSystem:
    def __init__(self, db_path="./milvus_rag.db", collection_name="rag_collection"):
        print("Initializing Milvus client with GPU support...")
        self.client = MilvusClient(uri=db_path)
        self.collection_name = collection_name
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self._init_collection()
        
    def _init_collection(self):
        
        if self.client.has_collection(self.collection_name):
            print(f"Collection '{self.collection_name}' exists. Dropping it.")
            self.client.drop_collection(self.collection_name)
        else:
            print(f"Collection '{self.collection_name}' does not exist. Creating a new one.")
            
       
        test_embedding = self._generate_embeddings("Test")
        embedding_dim = len(test_embedding)
        self.client.create_collection(
            collection_name=self.collection_name,
            dimension=embedding_dim,
            metric_type="IP",
            consistency_level="Strong"
        )
        print(f"Collection '{self.collection_name}' is ready.")
    
    def _generate_embeddings(self, text: str) -> list[float]:


        
        response = ollama.embeddings(
            model="mxbai-embed-large", 
            prompt=text
        )
        return response["embedding"]
    
    def _text_to_chunks(self, text: str, chunk_size: int = 512) -> list[str]:
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    def ingest_data(self, text: str):
        print("Starting data ingestion...")
        chunks = self._text_to_chunks(text)
        data = []
        for idx, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
            data.append({
                "id": id(text) + idx,  
                "vector": self._generate_embeddings(chunk),
                "text": chunk
            })
        self.client.insert(
            collection_name=self.collection_name,
            data=data
        )
        print("Data ingestion complete.")
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        
        results = self.client.search(
            collection_name=self.collection_name,
            data=[self._generate_embeddings(query)],
            limit=top_k,
            output_fields=["text"]
        )
        if not results or not results[0]:
            return ""
        return "\n".join(
            [hit["entity"]["text"] for hit in results[0]]
        )
    
    def generate_response(self, query: str) -> str:
        
        context = self.retrieve_context(query)
        if not context.strip():
            return "No relevant data found in the database for your query."
        
        
        chat_history = "\n".join(
            [f"{'Human' if isinstance(msg, HumanMessage) else 'AI'}: {msg.content}" 
             for msg in self.memory.load_memory_variables({}).get("chat_history", [])]
        )
        
       
        messages = []
        if chat_history:
            messages.append({
                "role": "system",
                "content": f"Previous conversation:\n{chat_history}"
            })
        messages.append({
            "role": "system",
            "content": f"Answer using this context: {context}"
        })
        messages.append({
            "role": "user",
            "content": query
        })
        
       
        response = ollama.chat(
            model="llama3.2",
            messages=messages
        )
        
        generated_response = response["message"]["content"]
        
       
        self.memory.chat_memory.add_user_message(query)
        self.memory.chat_memory.add_ai_message(generated_response)
        
        return generated_response

def extract_text_from_pdf(file_path):
    print("Extracting text from PDF...")
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def main():
    file_path = "/home/lenin/Downloads/402_IT_X.pdf" # give your desired input in this case i have chosen pdf file 
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    extracted_text = extract_text_from_pdf(file_path)
    
    print("Initializing RAG system...")
    rag = RAGSystem(collection_name="my_rag_collection")
    
    print("Ingesting extracted text into the database...")
    rag.ingest_data(extracted_text)
    
    print("\nSetup complete. Chatbot ready! Type your question (or 'exit' to quit):")
    while True:
        user_query = input("Your question: ")
        if user_query.lower() in ['exit', 'quit']:
            print("Exiting chatbot.")
            break
        response = rag.generate_response(user_query)
        print("Response:")
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()
