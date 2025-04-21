from langchain_experimental.text_splitter import SemanticChunker
from typing import List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

def split_docs(docs: List[Document], embedder: Embeddings) -> List[Document]:

    # Split into chunks using the SemanticChunker with the embedder
    text_splitter = SemanticChunker(embeddings=embedder)
    documents = text_splitter.split_documents(docs)

    return documents