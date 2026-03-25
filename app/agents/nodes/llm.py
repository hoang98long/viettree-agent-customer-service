from app.llms import get_llm

llm = get_llm()

def llm_node(state):
    state["answer"] = llm.invoke(state["question"])
    return state