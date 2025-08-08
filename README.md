# RAG Agent

LangGraph 기반의 RAG(Retrieval Augmented Generation) 시스템으로, 문서 기반 질의응답을 제공하는 FastAPI 서버입니다.

##  프로젝트 목표

개발자 팀이 협업 중 문서 기반 질의를 쉽게 해결할 수 있도록 하는 중앙관리 Agent입니다. 과제 정의서와 요구사항 정의서를 기반으로 사용자의 질문에 적절한 답변을 제공합니다.

##  시스템 아키텍처

### RAG 파이프라인
```
사용자 질문 → Input Node → Retrieve Node → Generate Node → 답변
```

- **Input Node**: 사용자 질문 처리
- **Retrieve Node**: 벡터 데이터베이스에서 관련 문서 검색
- **Generate Node**: OpenAI GPT를 활용한 답변 생성

##  프로젝트 구조

```
rag_agent/
├── main.py                 # FastAPI 서버 메인 파일
├── requirements.txt        # Python 의존성 패키지
├── step1_test.py          # 테스트 파일
├── app/                   # 핵심 애플리케이션 로직
│   ├── __init__.py
│   ├── graph.py           # LangGraph 워크플로우 정의
│   ├── loader.py          # 문서 로드 및 분할
│   ├── state.py           # RAG 상태 관리
│   ├── store.py           # 글로벌 벡터 스토어 관리
│   ├── vector_store.py    # FAISS 벡터 스토어 생성
│   └── nodes/             # LangGraph 노드들
│       ├── input_node.py      # 입력 처리 노드
│       ├── retrieve_node.py   # 문서 검색 노드
│       └── generate_node.py   # 답변 생성 노드
└── data/                  # 업로드된 문서 저장 디렉토리
    └── project_overview.txt
```

##  설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 서버 실행
```bash
uvicorn main:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

##  API 엔드포인트

### 1. 질문하기
**POST** `/ask`
```json
{
    "question": "프로젝트의 목표가 무엇인가요?"
}
```

### 2. 파일 업로드
**POST** `/upload`
- 파일을 업로드하고 자동으로 벡터 인덱싱을 수행합니다.
- 지원 형식: `.txt`, `.pdf`

### 3. 문서 목록 조회
**GET** `/list_docs`
- 업로드된 문서들의 ID 목록을 반환합니다.

### 4. 문서 전체 삭제
**POST** `/clear_docs`
- 벡터 스토어와 업로드된 모든 문서를 초기화합니다.

##  주요 기능

### 문서 처리
- **지원 형식**: TXT, PDF
- **자동 청킹**: RecursiveCharacterTextSplitter로 문서를 적절한 크기로 분할
- **벡터화**: OpenAI Embeddings를 사용한 의미 벡터화

### 검색 시스템
- **벡터 데이터베이스**: FAISS 기반 고속 유사도 검색
- **Top-K 검색**: 관련도가 높은 상위 3개 문서 청크 검색

### 답변 생성
- **LLM**: OpenAI ChatGPT 모델 사용
- **한국어 지원**: 한국어 프롬프트와 답변 생성
- **컨텍스트 기반**: 검색된 문서를 바탕으로 정확한 답변 생성

##  기술 스택

- **프레임워크**: FastAPI, LangGraph
- **LLM**: OpenAI GPT
- **벡터 데이터베이스**: FAISS
- **문서 처리**: LangChain Community
- **임베딩**: OpenAI Embeddings

##  사용 예시

1. **문서 업로드**:
   ```bash
   curl -X POST "http://localhost:8000/upload" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@your_document.pdf"
   ```

2. **질문하기**:
   ```bash
   curl -X POST "http://localhost:8000/ask" \
        -H "Content-Type: application/json" \
        -d '{"question": "프로젝트의 주요 기능은 무엇인가요?"}'
   ```

##  워크플로우

1. 사용자가 문서를 업로드
2. 시스템이 문서를 청킹하고 벡터화하여 FAISS 인덱스에 저장
3. 사용자가 질문을 전송
4. LangGraph가 다음 순서로 처리:
   - **Input Node**: 질문 전처리
   - **Retrieve Node**: 관련 문서 검색
   - **Generate Node**: 컨텍스트 기반 답변 생성
5. 사용자에게 답변 반환

##  향후 개발 계획

- 다양한 문서 형식 지원 확장 (DOCX, PPTX 등)
- 대화 히스토리 관리
- 멀티모달 지원 (이미지, 표 등)
- 사용자별 문서 관리
- 실시간 문서 업데이트 감지

##  라이선스

이 프로젝트는 개발팀 내부용으로 제작되었습니다.

##  기여하기

프로젝트에 기여하고 싶으시다면 이슈를 생성하거나 풀 리퀘스트를 보내주세요.
