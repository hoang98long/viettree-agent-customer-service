from app.agents import graph

def ask_agent(question: str) -> str:
    result = graph.invoke({"question": question})
    return result["answer"]