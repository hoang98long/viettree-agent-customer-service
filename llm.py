from langchain_community.llms import Ollama

def get_llm():
    return Ollama(
        model="qwen3-vl:4b",   # hoặc mistral
        temperature=0
    )
