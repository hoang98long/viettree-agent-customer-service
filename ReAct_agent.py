from typing import TypedDict, Annotated, Sequence
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    message: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
    """add 2 numbers function"""
    return a + b

tools = [add]

model = ChatOllama(
    model="qwen2.5:7b"
).bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_promt = SystemMessage(
        content="You are my AI assistant, please answer my query to the best of your ability"
    )
    respone = model.invoke([system_promt] + state["message"])
    return {"message": [respone]}

def should_continue(state: AgentState):
    messages = state["message"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("agent", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

graph.add_edge("tools", "agent")
agent = graph.compile
def print_stream(stream):
    for s in stream:
        message = s["message"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {
    "message": [("user", "Add 10 + 10")]
}
print_stream(agent.stream(inputs, stream_mode="values"))