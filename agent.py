
"""
Customer Support Agent using LangGraph with RAG + Ollama.

Uses:
    - Ollama for local LLM inference
    - Ollama embeddings for local RAG
    - FAISS for vector search
    - LangGraph for agent orchestration

Prerequisites:
    ollama pull qwen3:8b
    ollama pull nomic-embed-text

Usage:
    python agent.py
    python agent.py --kb-dir docs/
"""

import argparse
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_BASE_URL = "http://localhost:11434"

# Your locally installed model
LLM_MODEL = "qwen3:8b"

# Pull this model with:
# ollama pull nomic-embed-text
EMBEDDING_MODEL = "nomic-embed-text"


# ---------------------------------------------------------------------------
# Escalation Rules
# ---------------------------------------------------------------------------

ESCALATION_KEYWORDS = [
    "refund",
    "lawsuit",
    "furious",
    "fraud",
    "broken",
    "data loss",
    "cancel account",
    "charge",
    "billing error",
]


# ---------------------------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------------------------

class SupportState(TypedDict):
    messages: Annotated[list, add_messages]
    user_input: str
    retrieved_context: str
    response: str
    escalate: bool


# ---------------------------------------------------------------------------
# RAG Retrieval
# ---------------------------------------------------------------------------

def retrieve_context(state: SupportState) -> SupportState:
    """
    Retrieve the most relevant knowledge-base documents using
    local Ollama embeddings + FAISS.
    """

    query = state["user_input"]

    # Create the vector store only once.
    if not hasattr(retrieve_context, "vectorstore"):

        texts = getattr(
            retrieve_context,
            "kb_texts",
        )

        print("\n[Initializing local Ollama embeddings...]")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20,
        )

        docs_split = splitter.create_documents(texts)

        embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL,
        )

        retrieve_context.vectorstore = FAISS.from_documents(
            docs_split,
            embeddings,
        )

        print("[Vector store ready]")

    docs = retrieve_context.vectorstore.similarity_search(
        query,
        k=3,
    )

    context = "\n".join(
        f"- {doc.page_content}"
        for doc in docs
    )

    return {
        "retrieved_context": context,
    }


# ---------------------------------------------------------------------------
# Escalation Check
# ---------------------------------------------------------------------------

def check_escalation(state: SupportState) -> SupportState:
    """
    Determine whether the customer's issue should be escalated.
    """

    text = state["user_input"].lower()

    needs_escalation = any(
        keyword in text
        for keyword in ESCALATION_KEYWORDS
    )

    return {
        "escalate": needs_escalation,
    }


# ---------------------------------------------------------------------------
# Response Generation
# ---------------------------------------------------------------------------

def generate_response(state: SupportState) -> SupportState:
    """
    Generate a response using the local Ollama model.
    """

    conversation = state["messages"][:-1]

    # ---------------------------------------------------------------
    # Escalated request
    # ---------------------------------------------------------------

    if state.get("escalate"):

        response_text = (
            "I understand your concern and I want to make sure "
            "this gets the attention it deserves. I'm connecting "
            "you with a senior support specialist who can resolve "
            "this directly. You'll hear back within 2 hours. "
            "Your case ID is #"
            + str(hash(state["user_input"]) % 100000)
            + "."
        )

    # ---------------------------------------------------------------
    # Normal RAG response
    # ---------------------------------------------------------------

    else:

        llm = ChatOllama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.2,
        )

        system_prompt = f"""
You are a helpful customer support agent for a company.

Use ONLY the knowledge-base context below when answering
questions about the provided document.

Knowledge Base:
{state["retrieved_context"]}

Instructions:
- Be friendly and concise.
- Give practical troubleshooting steps.
- Do not invent product features, prices, policies, or limits.
- If the knowledge base does not contain the answer, say that
  you do not have enough information and recommend contacting support.
- Do not mention that you are using RAG, FAISS, Ollama, or a vector database.
"""

        messages = [
            SystemMessage(content=system_prompt),
            *conversation,
            HumanMessage(content=state["user_input"]),
        ]

        response = llm.invoke(messages)

        response_text = response.content

    return {
        "response": response_text,
        "messages": [
            AIMessage(content=response_text)
        ],
    }


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def route_after_escalation_check(
    state: SupportState,
) -> Literal["generate"]:
    return "generate"


# ---------------------------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------------------------

def build_graph():

    graph = StateGraph(SupportState)

    graph.add_node(
        "retrieve",
        retrieve_context,
    )

    graph.add_node(
        "check_escalation",
        check_escalation,
    )

    graph.add_node(
        "generate",
        generate_response,
    )

    graph.set_entry_point("retrieve")

    graph.add_edge(
        "retrieve",
        "check_escalation",
    )

    graph.add_edge(
        "check_escalation",
        "generate",
    )

    graph.add_edge(
        "generate",
        END,
    )

    return graph.compile()


# ---------------------------------------------------------------------------
# Knowledge Base Loader
# ---------------------------------------------------------------------------

def load_kb_texts(kb_dir: str | None) -> list[str]:

    if not kb_dir:
        return SAMPLE_KB

    root = Path(kb_dir)

    if not root.is_dir():
        raise ValueError(
            f"Knowledge base directory does not exist: {kb_dir}"
        )

    texts = []

    for path in sorted(root.rglob("*")):

        if (
            path.is_file()
            and path.suffix.lower() in {".txt", ".md"}
        ):
            texts.append(
                path.read_text(
                    encoding="utf-8"
                )
            )

    if not texts:
        raise ValueError(
            f"No .txt or .md files found in knowledge base directory: {kb_dir}"
        )

    return texts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Customer Support Agent using Ollama"
    )

    parser.add_argument(
        "--kb-dir",
        help="Directory containing .txt or .md support knowledge base files",
    )

    args = parser.parse_args()

    # Load knowledge base
    retrieve_context.kb_texts = load_kb_texts(
        args.kb_dir
    )

    # Rebuild vector store if main() is run again
    if hasattr(retrieve_context, "vectorstore"):
        delattr(
            retrieve_context,
            "vectorstore",
        )

    print("\n" + "=" * 60)
    print("🎧 Customer Support Agent")
    print("=" * 60)
    print(f"LLM:        {LLM_MODEL}")
    print(f"Embeddings: {EMBEDDING_MODEL}")
    print(f"Ollama:     {OLLAMA_BASE_URL}")
    print("=" * 60)
    print("Type 'quit' to exit\n")

    agent = build_graph()

    state: SupportState = {
        "messages": [],
        "user_input": "",
        "retrieved_context": "",
        "response": "",
        "escalate": False,
    }

    while True:

        user_input = input("Customer: ").strip()

        if user_input.lower() in (
            "quit",
            "exit",
            "q",
        ):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        state["user_input"] = user_input

        state["messages"].append(
            HumanMessage(
                content=user_input
            )
        )

        try:

            state = agent.invoke(state)

            escalation_indicator = (
                " [ESCALATED]"
                if state.get("escalate")
                else ""
            )

            print(
                f"\nAgent{escalation_indicator}: "
                f"{state['response']}\n"
            )

        except Exception as exc:

            print(
                "\n❌ Error:",
                exc,
                "\n",
            )


if __name__ == "__main__":
    main()