# app/agents/multi_agent_graph.py

from langgraph.graph import StateGraph
from app.llms import get_llm
from app.rag import build_retriever

llm = get_llm()
retriever = build_retriever()

class State(dict): pass


def router_node(state):
    q = state["question"].lower()

    if "giá" in q or "mua" in q:
        return "sales"
    elif "lỗi" in q or "không chạy" in q:
        return "support"
    else:
        return "llm"


def sales_agent(state):
    state["answer"] = llm.invoke(f"Tư vấn bán hàng: {state['question']}")
    return state


def support_agent(state):
    docs = retriever.get_relevant_documents(state["question"])
    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
Bạn là kỹ thuật viên.
{context}
Câu hỏi: {state['question']}
"""
    state["answer"] = llm.invoke(prompt)
    return state


def llm_agent(state):
    state["answer"] = llm.invoke(state["question"])
    return state


builder = StateGraph(State)

builder.add_node("sales", sales_agent)
builder.add_node("support", support_agent)
builder.add_node("llm", llm_agent)

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    router_node,
    {
        "sales": "sales",
        "support": "support",
        "llm": "llm"
    }
)

builder.set_finish_point("sales")
builder.set_finish_point("support")
builder.set_finish_point("llm")

graph = builder.compile()