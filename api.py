from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain_core.messages import HumanMessage, AIMessage

from agent import (
    SupportState,
    build_graph,
    load_kb_texts,
    retrieve_context,
)


# ---------------------------------------------------------
# App
# ---------------------------------------------------------

app = FastAPI(
    title="Customer Support API"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Frontend
# ---------------------------------------------------------

app.mount(
    "/ui",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)


# ---------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------

retrieve_context.kb_texts = load_kb_texts("docs")

if hasattr(retrieve_context, "vectorstore"):
    delattr(retrieve_context, "vectorstore")


agent = build_graph()


# ---------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []


class ChatResponse(BaseModel):
    response: str
    escalated: bool


# ---------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    messages = []

    for item in request.history:

        if item["role"] == "user":
            messages.append(
                HumanMessage(
                    content=item["content"]
                )
            )

        elif item["role"] == "assistant":
            messages.append(
                AIMessage(
                    content=item["content"]
                )
            )

    # Current user message
    messages.append(
        HumanMessage(
            content=request.message
        )
    )

    state: SupportState = {
        "messages": messages,
        "user_input": request.message,
        "retrieved_context": "",
        "response": "",
        "escalate": False,
    }

    result = agent.invoke(state)

    return ChatResponse(
        response=result["response"],
        escalated=result.get("escalate", False),
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }
