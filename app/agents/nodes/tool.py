from app.tools.product_tools import get_price, check_stock

def tool_node(state):
    q = state["question"]

    if "giá" in q:
        state["answer"] = get_price()
    elif "còn hàng" in q:
        state["answer"] = check_stock()

    return state