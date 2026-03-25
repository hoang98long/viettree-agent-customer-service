from app.llms import get_llm

llm = get_llm()

def critic_node(state):
    feedback = llm.invoke(f"""
Đánh giá câu trả lời:
Q: {state['question']}
A: {state['answer']}

Trả lời "yes" nếu đúng, "no" nếu sai.
""")

    if "no" in feedback.lower():
        return "fix"
    return "ok"