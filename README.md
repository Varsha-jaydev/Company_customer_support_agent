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
```
