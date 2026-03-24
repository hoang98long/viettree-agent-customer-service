from langgraph.graph import StateGraph

from app.llms import get_llm
from app.rag import build_retriever

llm = get_llm()
retriever = build_retriever()

class State(dict):
    pass

def retrieve_node(state):
    docs = retriever.get_relevant_documents(state["question"])
    state["docs"] = docs
    return state

def router_node(state):
    return "faq" if state["docs"] else "llm"

def faq_node(state):
    context = "\n".join([d.page_content for d in state["docs"]])

    prompt = f"""
Bạn là AI tư vấn sản phẩm.
Chỉ trả lời dựa trên dữ liệu sau:

{context}

Câu hỏi: {state['question']}
"""

    state["answer"] = llm.invoke(prompt)
    return state

def llm_node(state):
    state["answer"] = llm.invoke(state["question"])
    return state


builder = StateGraph(State)

builder.add_node("retrieve", retrieve_node)
builder.add_node("faq", faq_node)
builder.add_node("llm", llm_node)

builder.set_entry_point("retrieve")

builder.add_conditional_edges(
    "retrieve",
    router_node,
    {"faq": "faq", "llm": "llm"}
)

builder.set_finish_point("faq")
builder.set_finish_point("llm")

graph = builder.compile()