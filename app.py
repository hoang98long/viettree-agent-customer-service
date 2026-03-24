from fastapi import FastAPI
from graph import graph

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/ask")
def ask(question: str):
    result = graph.invoke({"question": question})
    return {"answer": result["answer"]}
