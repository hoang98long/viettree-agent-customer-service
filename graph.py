from langgraph.graph import StateGraph
from llm import get_llm
from rag import build_retriever

llm = get_llm()
retriever = build_retriever()

class State(dict):
    pass


# STEP 1: retrieve FAQ
def retrieve_node(state):
    question = state["question"]
    docs = retriever.get_relevant_documents(question)
    state["docs"] = docs
    return state


# STEP 2: router
def router_node(state):
    if len(state["docs"]) > 0:
        return "faq"
    return "llm"


# STEP 3: FAQ answer
def faq_node(state):
    context = "\n".join([doc.page_content for doc in state["docs"]])

    prompt = f"""
Bạn là AI tư vấn sản phẩm.

Chỉ trả lời dựa trên thông tin sau:
{context}

Câu hỏi: {state['question']}
"""

    answer = llm.invoke(prompt)
    state["answer"] = answer
    return state


# STEP 4: fallback LLM
def llm_node(state):
    answer = llm.invoke(state["question"])
    state["answer"] = answer
    return state


# BUILD GRAPH
builder = StateGraph(State)

builder.add_node("retrieve", retrieve_node)
builder.add_node("faq", faq_node)
builder.add_node("llm", llm_node)

builder.set_entry_point("retrieve")

builder.add_conditional_edges(
    "retrieve",
    router_node,
    {
        "faq": "faq",
        "llm": "llm"
    }
)

builder.set_finish_point("faq")
builder.set_finish_point("llm")

graph = builder.compile()
