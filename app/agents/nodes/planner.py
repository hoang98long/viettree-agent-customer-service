from app.llms import get_llm

llm = get_llm()

def planner_node(state):
    plan = llm.invoke(f"""
Chia câu hỏi thành các bước nhỏ:
{state['question']}
""")

    state["plan"] = [p for p in plan.split("\n") if p.strip()]
    return state