# 🤖 Company Customer Support Agent

An AI-powered, customizable customer support agent built with **LangGraph, LangChain, Ollama, FAISS, RAG, FastAPI, and HTML/CSS/JavaScript**.

The main idea is simple:

> **Add your company's support information to the `docs/` folder, start the application, and the AI agent uses that information to answer customer questions.**

You can use this project for your own company, product, SaaS application, internal support system, or personal AI-agent experiments.

---

## ✨ Features

* 🤖 Local LLM using **Ollama**
* 🧠 Qwen3 for response generation
* 📚 Custom company knowledge base
* 🔎 Retrieval-Augmented Generation (RAG)
* 🧩 FAISS vector similarity search
* 🔤 Ollama embeddings with `nomic-embed-text`
* 🔄 LangGraph agent workflow
* 🚨 Automatic escalation detection
* 💬 Conversation history
* ⚡ FastAPI backend
* 🌐 Simple browser-based chat UI
* 📖 Swagger API documentation
* 🔒 Local AI inference
* 🏢 **Easy company-specific customization**

---

# 🎯 How It Works

The project is designed so that you don't need to modify the AI logic every time you want to use it for a different company.

Simply update the documents inside:

```text
docs/
```

For example:

```text
docs/
├── company_info.md
├── products.md
├── pricing.md
├── troubleshooting.md
├── billing.md
├── refund_policy.md
└── faq.md
```

The application automatically loads these documents and creates a searchable knowledge base.

### Architecture

```text
                  ┌───────────────────────┐
                  │       Customer        │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │      Chat UI          │
                  │   HTML/CSS/JS         │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │       FastAPI         │
                  │       /chat           │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │      LangGraph        │
                  │    Agent Workflow     │
                  └───────────┬───────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
       ┌────────────────┐          ┌─────────────────┐
       │ RAG Retrieval  │          │ Escalation Check│
       └───────┬────────┘          └─────────────────┘
               │
               ▼
       ┌────────────────┐
       │      FAISS     │
       │ Vector Search  │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ Ollama         │
       │ Embeddings     │
       │ nomic-embed    │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ Ollama         │
       │ Qwen3:8b       │
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ AI Response    │
       └────────────────┘
```

# 🛠️ Technology Stack

| Technology          | Purpose                 |
| ------------------- | ----------------------- |
| Python              | Core application        |
| LangGraph           | Agent orchestration     |
| LangChain           | LLM and RAG integration |
| Ollama              | Local AI inference      |
| Qwen3:8b            | Chat model              |
| nomic-embed-text    | Embeddings              |
| FAISS               | Vector search           |
| FastAPI             | Backend API             |
| Uvicorn             | API server              |
| Pydantic            | Request validation      |
| HTML/CSS/JavaScript | Web UI                  |



# 📝 Add Your Company Information

This is the most important step.

Go to:

```text
docs/
```

Remove the example documents if necessary and add your own `.md` or `.txt` files.

For example:

```text
docs/
├── company_info.md
├── products.md
├── pricing.md
├── support.md
├── policies.md
└── faq.md
```

---

# ▶️ Start the Application

Run:

```bash
uvicorn api:app --reload
```

You should see:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 🌐 Open the Customer Support UI

Open:

```text
http://127.0.0.1:8000/ui/
```

You will see the customer-support chat interface.

You can then ask questions based on your company's documentation.

---

# 🖥️ Screenshots

## 💬 Customer Support Chat UI

The browser-based customer support interface allows users to interact with the AI agent using natural language.

![Customer Support Chat UI](docs/images/chat-ui.png)


# ⭐ Project Goal

The goal of this project is to provide a simple starting point for building **custom AI customer-support agents using local LLMs and company-specific knowledge**.

Instead of building a completely new AI application for every company:

```text
Same AI Agent
      +
Different docs/
      =
Different Customer Support Agent
```

---

# 👩‍💻 Author

**Varsha Jaydev**

GitHub:

[Varsha Jaydev on GitHub](https://github.com/Varsha-jaydev?utm_source=chatgpt.com)

---

## ⭐ If you find this project useful

Give the repository a ⭐ on GitHub and feel free to adapt it for your own company or project.
