from langchain_core.vectorstores import VectorStoreRetriever, VectorStore


def retrieve(saved_vector: VectorStore) -> VectorStoreRetriever:
    
    retriever = saved_vector.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 1}
        )
    return retriever