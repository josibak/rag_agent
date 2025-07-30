from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_graph
from fastapi import UploadFile, File
from app.loader import load_documents, split_documents
from app.vector_store import create_vector_store
from app.store import global_vector_store

class QuestionRequest(BaseModel):
    question: str

rag_graph = build_graph()
app = FastAPI()

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    result = rag_graph.invoke({"question": req.question})
    return {
        "question": req.question,
        "answer": result["answer"]
    }

global_vector_store = create_vector_store(split_documents(load_documents("data/")))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    save_path = f"data/{file.filename}"
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # store 모듈의 글로벌 객체를 갱신
    docs = load_documents("data/")
    store.global_vector_store = create_vector_store(split_documents(docs))

    return {"message": f"{file.filename} 업로드 및 벡터 인덱싱 완료"}