from app.rag import build_retriever

retriever = build_retriever()

def retrieve_node(state):
    docs = retriever.similarity_search_with_score(
        state["question"], k=3
    )

    state["docs"] = docs
    return state