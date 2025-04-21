import os
from langchain_community.vectorstores import FAISS
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings




vector_store_path = "/Users/abubakarmuktar/Documents/Think-Cell/VectorStoreDB"
index_name = "faiss_index"
full_index_path = os.path.join(vector_store_path, index_name)


def embed_docs(documents: List[Document], embedder: Embeddings) -> FAISS:
    # Ensure the directory exists
    os.makedirs(vector_store_path, exist_ok=True)

    # just query if it exists
    if os.path.exists(full_index_path):
        saved_vector = FAISS.load_local(full_index_path, 
                                        embeddings=embedder, 
                                        allow_dangerous_deserialization=True)

        return saved_vector
    else:
        embedded_vector = FAISS.from_documents(documents=documents, embedding=embedder)
        embedded_vector.save_local(full_index_path)
        
        return embedded_vector