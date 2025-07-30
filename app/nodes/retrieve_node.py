from app.vector_store import create_vector_store
from app.loader import load_documents, split_documents

from app.store import global_vector_store
# 전역 벡터스토어 생성 (실제 프로젝트에서는 캐시 또는 persistence 권장)
# documents = load_documents("data/")
# split_docs = split_documents(documents)
# vector_store = create_vector_store(split_docs)

def retrieve_node(state):
    question = state.question
    docs = global_vector_store.similarity_search(question, k=3)
    return {**state.dict(), "retrieved_docs": docs}
