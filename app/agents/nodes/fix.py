from app.llms import get_llm

llm = get_llm()

def fix_node(state):
    improved = llm.invoke(f"""
Cải thiện câu trả lời sau:
{state['answer']}
""")

    state["answer"] = improved
    return state