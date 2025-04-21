
# Rethinking Support at think-cell: A RAG-Based Chatbot

This project is a prototype support chatbot designed to assist users with think-cell's documentation in real time. It demonstrates how Retrieval-Augmented Generation (RAG) techniques can be used to enhance user support by delivering accurate, document-aware responses.

## 🧠 How It Works

- **Data Source**:  
  The think-cell [Knowledge Base](https://www.think-cell.com/en/support/) and [User Manual](https://www.think-cell.com/en/resources/manual/) were crawled to collect support-related content.

- **Extraction**:  
  Relevant information was parsed using **BeautifulSoup**, structured for indexing, and formatted for semantic search.

- **Model**:  
  The chatbot is powered by the **Mistral 7B** language model, hosted locally using the **Ollama** server.

- **Architecture**:  
  A **Retrieval-Augmented Generation (RAG)** pipeline enables the model to:
  - Search the indexed support data for relevant content.
  - Generate grounded, context-aware responses using those documents.

---

## 🔧 Tech Stack

- `Python`
- `BeautifulSoup` for HTML parsing
- `Ollama` for model serving
- `Mistral 7B` as the LLM
- `RAG` for retrieval + generation
- `Gradio` for UI

---

## 🤝 Purpose

This was not developed as part of any formal test or prompt from think-cell. It’s a personal initiative to explore how AI can augment customer support for complex, high-value software.

I'm open to contributing to the think-cell team in any capacity—freelance, intern, or collaborator.


## 📝 License

This project is for demonstration and educational purposes only. Not affiliated with or endorsed by think-cell.

---

Let me know if you’d like to include code setup instructions or API endpoints!
