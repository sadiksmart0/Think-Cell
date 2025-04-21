import gradio as gr
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from load_data import load_data
from split_text import split_docs
from embed_docs import embed_docs
from query_response import get_response
from retrieve import retrieve
from js import js
from theme import theme
import os

URL = "https://www.think-cell.com/en/resources/kb/overview.fcgi"
BASE_URL = "https://www.think-cell.com/en/resources/"
vector_store_path = "/Users/abubakarmuktar/Documents/Think-Cell/VectorStoreDB"
index_name = "faiss_index"
full_index_path = os.path.join(vector_store_path, index_name)


# Define the prompt template
prompt = """
1. You are Mariam, a CUSTOMER SUPPORT ENGINEER helping Think-cell's customers answer questions related to their software product, use the following pieces of context to answer the question at the end.
2. If you don't know the answer, just say that "I don't know, you may have to contact CUSTOMER SUPPORT" but don't make up an answer on your own.
3. Keep the answer crisp and straight forward.
4. Add the LINKS for the particular sources for easy accessibility.

Context: {context}

Question: {{question}}

Helpful Answer:"""

# Create the embedder with a specific model
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define llm
llm = OllamaLLM(
    model="mistral:instruct",
  )

chunks = None
# just query if it exists
if not os.path.exists(full_index_path):
  docs = load_data(URL, BASE_URL) #Load Dataset
  chunks = split_docs(docs, embedder=embedder) #Split Document

saved_vector = embed_docs(chunks, embedder=embedder) #Embed Document
retrieved = retrieve(saved_vector) # Retrieve simimlar docs



QA_CHAIN_PROMPT = PromptTemplate.from_template(template=prompt)

# Create document prompt
document_prompt = PromptTemplate(
    input_variables=["page_content", "source"],
    template="Context:\ncontent:{page_content}\nsource:{source}",
)

# Create the stuff documents chain
combine_docs_chain = create_stuff_documents_chain(
    llm,
    QA_CHAIN_PROMPT,
    document_prompt=document_prompt
)

# Create the retrieval chain
qa_chain = create_retrieval_chain(
    retriever=retrieved,
    combine_docs_chain=combine_docs_chain
)

#----------------------------SEND TO CHAT----------------------------#
def send_to_chat(question: str, history) -> str:
    return get_response(question, qa_chain)


#----------------------------GRADIO INTERFACE----------------------------#
with gr.Blocks(title="CUSTOMER SUPPORT AGENT", theme=theme, js=js) as demo:
    
    with gr.Row():
        with gr.Column():
            gr.Image("Resources/Logo1.jpeg", height=60, elem_id="logo", show_label=False,show_download_button=False)
            gr.Markdown("Think-cell Knowledge Base Chatbot")
            gr.Markdown("# Got a Problem? Just Ask Me!! I am Mariam 👸🏽. Your bot Service Agent🤗")

            chat = gr.ChatInterface(
                send_to_chat,
                chatbot=gr.Chatbot(height=450, type="messages"),
                textbox=gr.Textbox(
                    placeholder="Seeking For Answer? Ask Our Support Agent", 
                    container=True,
                    scale=7,
                    submit_btn=True,
                    type="text"
                ),
                title="Customer Support Agent",
                examples=["How do I report a problem to think-cell?",
                           "How can I create a linear trendline in a line chart?",
                           "Segment colors in think-cell charts do not update when I apply conditional formatting to a cell in Excel?"],
                cache_examples=True
            )


if __name__ == "__main__":
  demo.launch(share=True, debug=True)
