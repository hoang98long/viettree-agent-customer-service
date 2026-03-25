from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_router(state):
    q = state["question"]

    q_emb = model.encode(q)

    sales_emb = model.encode("hỏi giá sản phẩm mua hàng")
    support_emb = model.encode("lỗi sản phẩm kỹ thuật")

    if cosine(q_emb, sales_emb) > 0.7:
        return "sales"

    if cosine(q_emb, support_emb) > 0.7:
        return "support"

    return "general"