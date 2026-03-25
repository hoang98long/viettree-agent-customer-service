from app.agents import graph

def ask_agent(question: str):
    state = {
        "question": question,
        "docs": [],
        "plan": [],
        "answer": ""
    }

    result = graph.invoke(state)
    return result["answer"]