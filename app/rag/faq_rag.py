from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.embeddings.hf import get_embeddings
from app.vectorstores.faiss_store import build_vectorstore

def build_retriever():
    loader = TextLoader("data/faq.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )

    split_docs = splitter.split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = build_vectorstore(split_docs, embeddings)

    return vectorstore.as_retriever()