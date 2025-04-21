# Invoke function
def get_response(question: str, chain) -> str:
    # Invoke the chain with the question
    result = chain.invoke({"input": question})
    
    # Return the answer
    return result["answer"]