# 🎧 Custom Customer Support Agent

An AI-powered customer support agent built with **LangGraph, LangChain, Ollama, FAISS, FastAPI, and a lightweight HTML/CSS/JavaScript frontend**.

The application combines **Retrieval-Augmented Generation (RAG)** with a local LLM to answer customer questions from a knowledge base while automatically identifying issues that require human escalation.

Everything can run locally using Ollama.

---

## ✨ Features

* 🤖 Local LLM inference with **Ollama**
* 🧠 **Qwen3 8B** for response generation
* 🔎 Retrieval-Augmented Generation (RAG)
* 📚 Local `.txt` and `.md` knowledge-base documents
* 🧩 **FAISS** vector similarity search
* 🔤 **Nomic Embed Text** embeddings
* 🔄 **LangGraph** agent orchestration
* 🚨 Automatic escalation detection
* 💬 Conversation history
* ⚡ FastAPI REST API
* 🌐 Browser-based chat interface
* 📖 Interactive Swagger API documentation
* 🔒 Runs locally without requiring a cloud LLM API

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Web Browser     │
                         │  HTML/CSS/JavaScript │
                         └──────────┬───────────┘
                                    │
                                    │ POST /chat
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │       api.py         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LangGraph      │
                         │    Agent Workflow   │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
              ┌──────────┐   ┌────────────┐   ┌───────────┐
              │  FAISS   │   │ Escalation │   │  Ollama   │
              │  Search  │   │   Check    │   │  Qwen3    │
              └────┬─────┘   └────────────┘   └─────┬─────┘
                   │                                  │
                   ▼                                  │
             ┌──────────────┐                         │
             │ Ollama       │                         │
             │ Embeddings   │                         │
             │ nomic-embed  │                         │
             └──────────────┘                         │
                   │                                  │
                   └──────────────┬───────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ Customer Support │
                         │    Response      │
                         └──────────────────┘
```

---

# 🔄 Agent Workflow

The LangGraph workflow follows three main steps:

```text
Customer Message
       │
       ▼
┌──────────────┐
│   Retrieve   │
│  KB Context  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Check Escalation │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate Response│
└────────┬─────────┘
         │
         ▼
       END
```

### 1. Retrieve

The customer's question is converted into an embedding using:

```text
nomic-embed-text
```

FAISS then searches the knowledge base for the most relevant chunks.

The top three matching chunks are passed to the agent.

### 2. Escalation Check

The system checks whether the customer's message contains predefined escalation keywords such as:

* refund
* lawsuit
* furious
* fraud
* broken
* data loss
* cancel account
* charge
* billing error

If an escalation keyword is detected, the request is routed to a human-support escalation response.

### 3. Generate Response

For normal requests, the retrieved knowledge-base context is supplied to:

```text
Qwen3:8b
```

The model is instructed to answer using only the available knowledge-base information.

---

# 🧰 Technology Stack

| Technology          | Purpose                  |
| ------------------- | ------------------------ |
| Python              | Application language     |
| LangGraph           | Agent orchestration      |
| LangChain           | LLM/RAG integration      |
| Ollama              | Local model inference    |
| Qwen3 8B            | Local chat model         |
| Nomic Embed Text    | Text embeddings          |
| FAISS               | Vector similarity search |
| FastAPI             | REST API                 |
| Uvicorn             | ASGI server              |
| Pydantic            | API validation           |
| HTML/CSS/JavaScript | Frontend UI              |

---

# 📁 Project Structure

```text
13-customer-support-agent/
│
├── agent.py                 # LangGraph + RAG agent
├── api.py                   # FastAPI backend
│
├── frontend/
│   ├── index.html           # Chat interface
│   └── script.js            # Frontend API integration
│
├── docs/
│   ├── company_info.md      # Knowledge base
│   ├── troubleshooting.md
│   └── billing.md
│
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Prerequisites

Make sure the following are installed:

* Python 3.10+
* Git
* Ollama
* `uv` (recommended) or `pip`

---

# 🦙 Install Ollama

Install Ollama from the official website:

https://ollama.com/

After installation, verify it:

```bash
ollama --version
```

---

# 📥 Download the Models

Pull the chat model:

```bash
ollama pull qwen3:8b
```

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify the installed models:

```bash
ollama list
```

You should see both models.

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/13-customer-support-agent.git
```

Move into the project:

```bash
cd 13-customer-support-agent
```

---

## Option 1: Using uv

Create the virtual environment:

```bash
uv venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

---

## Option 2: Using pip

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 📚 Knowledge Base

The agent reads `.txt` and `.md` files from:

```text
docs/
```

Example:

```text
docs/
├── company_info.md
├── troubleshooting.md
└── billing.md
```

You can add your own support documentation.

The application automatically:

1. Loads the documents
2. Splits them into chunks
3. Creates embeddings
4. Builds a FAISS vector store
5. Retrieves relevant chunks for each question

---

# ▶️ Running the API

Start the FastAPI server:

```bash
uvicorn api:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 🌐 Open the Chat UI

Once the server is running, open:

```text
http://127.0.0.1:8000/ui/
```

You should see the CloudSync Pro Support chat interface.

Example:

```text
┌───────────────────────────────────────┐
│ 🤖 CloudSync Support                 │
│ ● Online                             │
├───────────────────────────────────────┤
│                                       │
│ 👋 Hi! Welcome to CloudSync Support. │
│ How can I help you today?            │
│                                       │
│              What is the company     │
│              name?              You │
│                                       │
│ The company name is NovaTech         │
│ Solutions GmbH.                 Bot │
│                                       │
├───────────────────────────────────────┤
│ Type your message...             ➤   │
└───────────────────────────────────────┘
```

---

# 📖 API Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

The main endpoint is:

```text
POST /chat
```

---

# 💬 Chat API

### Request

```json
{
  "message": "What is the company name?",
  "history": []
}
```

### Response

```json
{
  "response": "The company name is NovaTech Solutions GmbH.",
  "escalated": false
}
```

---

# 🚨 Escalation Example

Send:

```json
{
  "message": "I have a billing error and I want a refund.",
  "history": []
}
```

The escalation system detects keywords such as:

```text
billing error
refund
```

and marks the request as escalated:

```json
{
  "response": "I understand your concern and I want to make sure this gets the attention it deserves...",
  "escalated": true
}
```

---

# ❤️ Health Check

The API provides a health endpoint:

```text
GET /health
```

Example:

```json
{
  "status": "ok"
}
```

---

# 🧪 Testing

### Test the API with curl

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d "{\"message\":\"What is the company name?\",\"history\":[]}"
```

### Test health

```bash
curl http://127.0.0.1:8000/health
```

---

# 🔐 Privacy

This project is designed to run locally.

The default architecture uses:

```text
Browser
   ↓
FastAPI
   ↓
LangGraph
   ↓
Ollama
   ↓
Local models
```

No external LLM API is required for the default setup.

---

# ⚠️ Current Limitations

This project is intended as an educational/portfolio implementation.

Current limitations include:

* Escalation is keyword-based.
* FAISS is initialized in memory.
* Vector indexes are rebuilt when the application initializes.
* Authentication is not implemented.
* No persistent conversation database is included.
* No production monitoring is included.
* The frontend is intentionally lightweight.
* The support knowledge base determines the factual content available to the agent.

---

# 🔮 Future Improvements

Potential improvements include:

* [ ] Persistent FAISS index
* [ ] PostgreSQL conversation storage
* [ ] User authentication
* [ ] Streaming LLM responses
* [ ] Better semantic escalation detection
* [ ] Confidence-based escalation
* [ ] Human-agent dashboard
* [ ] Conversation analytics
* [ ] RAG evaluation
* [ ] Automated tests
* [ ] Docker deployment
* [ ] Production logging
* [ ] Rate limiting
* [ ] Authentication and authorization
* [ ] Multi-tenant knowledge bases
* [ ] Source citations in responses

---

# 🧠 What This Project Demonstrates

This project demonstrates practical implementation of:

* Agentic AI
* Retrieval-Augmented Generation
* Local LLM inference
* Vector databases
* Embeddings
* LangGraph workflows
* API development
* Frontend/backend integration
* Conversation memory
* Rule-based escalation
* AI application architecture

---

# 📸 Demo

Add screenshots or a short GIF of the application here.

Recommended screenshots:

1. Chat UI
2. Swagger API documentation
3. Normal customer-support response
4. Escalated request
5. Project architecture

Example:

```text
docs/images/chat-ui.png
docs/images/swagger.png
docs/images/escalation.png
```

---

# 👩‍💻 Author

**Varshitha**

Built as part of an AI Agents project series exploring practical AI agent architectures with local LLMs and modern Python tooling.

---

# ⭐ If You Find This Useful

Feel free to star the repository and explore the other projects in the AI Agents series.
