# 03. LangChain 기초

LangChain 프레임워크의 핵심 개념과 사용법을 학습합니다.

## 📚 학습 내용

### 1. 환경 설정 및 모델 준비
- OpenAI/Ollama 설정
- API 키 관리

### 2. LLM 및 기본 템플릿
- ChatOpenAI, ChatOllama 사용
- 파라미터 설정 (temperature, max_tokens)
- 프롬프트 템플릿 (ChatPromptTemplate)
- 메시지 타입 (HumanMessage, SystemMessage, AIMessage)

### 3. LCEL (LangChain Expression Language)과 체인
- Runnable 프로토콜
- 파이프(`|`) 연산자로 체인 구성
- `.invoke()`, `.batch()`, `.stream()` 메소드

### 4. 메모리
- ConversationBufferMemory
- RunnableWithMessageHistory
- 대화 컨텍스트 유지
- 수동 메모리 관리

### 5. 출력 구조화를 위한 파서
- JsonOutputParser
- PydanticOutputParser
- 구조화된 데이터 추출

## 🚀 실행 방법

```bash
# Jupyter Notebook으로 열기
jupyter notebook 03_LangChain_기초.ipynb

# 또는 JupyterLab
jupyter lab 03_LangChain_기초.ipynb
```

## ⚙️ 필요 패키지

```bash
pip install langchain-core langchain-openai langchain-community pydantic
```

## 🎯 핵심 개념

### LCEL (LangChain Expression Language)
파이프 연산자로 컴포넌트를 연결하여 체인을 구성:

```python
chain = prompt_template | llm | output_parser
result = chain.invoke({"input": "..."})
```

### 메모리
대화 히스토리를 저장하고 관리:

```python
memory = ConversationBufferMemory(return_messages=True)
chain_with_memory = RunnableWithMessageHistory(...)
```

### Output Parser
LLM 출력을 구조화:

```python
# JSON 출력
json_chain = prompt | llm | JsonOutputParser()

# Pydantic 모델로 검증
pydantic_chain = prompt | llm | PydanticOutputParser(pydantic_object=MyModel)
```

## 💡 실습 예제

1. **기본 체인**: 프롬프트 → LLM → 파서
2. **메모리 체인**: 이전 대화를 기억하는 챗봇
3. **JSON 추출**: 텍스트에서 구조화된 정보 추출
4. **Pydantic 검증**: 특정 형식의 데이터 추출

## 📖 참고 자료

- [LangChain Documentation](https://python.langchain.com/)
- [LCEL Guide](https://python.langchain.com/docs/expression_language/)
- [Memory Types](https://python.langchain.com/docs/modules/memory/)

## 🔗 다음 단계

이 실습을 완료하면 **04. Streamlit 기초**로 넘어가
LangChain과 Streamlit을 결합한 대화형 앱을 만들 수 있습니다!

