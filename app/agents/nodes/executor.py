from app.llms import get_llm

llm = get_llm()

def executor_node(state):
    results = []

    for step in state.get("plan", []):
        result = llm.invoke(step)
        results.append(result)

    state["answer"] = "\n".join(results)
    return state