from langgraph.graph import StateGraph

from app.agents.nodes import (
    planner_node,
    executor_node,
    critic_node,
    fix_node,
    semantic_router,
    retrieve_node,
    faq_node,
    tool_node,
    llm_node
)

class State(dict):
    pass


builder = StateGraph(State)

# Nodes
builder.add_node("retrieve", retrieve_node)
builder.add_node("router", lambda x: x)
builder.add_node("faq", faq_node)
builder.add_node("tool", tool_node)
builder.add_node("llm", llm_node)
builder.add_node("planner", planner_node)
builder.add_node("executor", executor_node)
builder.add_node("critic", lambda x: x)
builder.add_node("fix", fix_node)

# Entry
builder.set_entry_point("retrieve")

# Routing
builder.add_conditional_edges(
    "retrieve",
    semantic_router,
    {
        "sales": "tool",
        "support": "faq",
        "general": "planner"
    }
)

# Planning flow
builder.add_edge("planner", "executor")

# Reflection
builder.add_conditional_edges(
    "executor",
    critic_node,
    {
        "ok": "end",
        "fix": "fix"
    }
)

builder.add_edge("fix", "end")
builder.add_edge("faq", "end")
builder.add_edge("tool", "end")
builder.add_edge("llm", "end")

graph = builder.compile()