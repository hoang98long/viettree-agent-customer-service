from app.llms import get_llm

llm = get_llm()

def faq_node(state):
    docs = state["docs"]

    context = "\n".join([doc[0].page_content for doc in docs])

    prompt = f"""
Bạn là AI tư vấn sản phẩm.
Chỉ dùng dữ liệu sau:

{context}

Câu hỏi: {state['question']}
"""

    state["answer"] = llm.invoke(prompt)
    return state