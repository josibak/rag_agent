from app.loader import load_documents, split_documents
from app.vector_store import create_vector_store

# 최초 생성 시점에 벡터스토어 초기화
documents = load_documents("data/")
split_docs = split_documents(documents)
global_vector_store = create_vector_store(split_docs)
