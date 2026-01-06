"""
rag_processor.py - PDF 파일 전처리 및 벡터 스토어 관리
=====================================================

학습 목표:
    1. PDF 파일 로딩 (PyMuPDFLoader)
    2. 텍스트 청킹 (RecursiveCharacterTextSplitter)
    3. 임베딩 생성 (OpenAIEmbeddings)
    4. 벡터 스토어 구축 (Chroma)
    5. 검색기 생성 (Retriever)
"""

import os
import tempfile
from pathlib import Path
from typing import Tuple, Optional, List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class RAGProcessor:
    """PDF 파일을 RAG 시스템용 벡터 스토어로 변환하는 클래스"""
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        self.api_key = api_key
        
        # YOUR CODE HERE - OpenAIEmbeddings 초기화
        # self.embeddings = OpenAIEmbeddings(
        #     model="text-embedding-3-small",
        #     api_key=api_key
        # )
        # 
        # 임베딩: 텍스트를 숫자 벡터로 변환하는 모델
        # text-embedding-3-small: OpenAI의 작고 빠른 임베딩 모델
        self.embeddings = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
        
        # YOUR CODE HERE - RecursiveCharacterTextSplitter 초기화
        # self.text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=800,
        #     chunk_overlap=200,
        #     length_function=len,
        #     separators=["\n\n", "\n", " ", ""]
        # )
        # 
        # chunk_size: 각 청크의 최대 크기 (800자)
        # chunk_overlap: 청크 간 중복 (200자) - 문맥 유지를 위해
        # separators: 분할 우선순위 (문단 → 줄 → 공백 → 글자)
        self.text_splitter = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
    
    def load_pdf(self, file_path: str) -> Tuple[List[Document], str]:
        """
        PDF 파일을 로드합니다.
        
        Args:
            file_path: PDF 파일 경로
            
        Returns:
            (문서 리스트, 상태 메시지)
        """
        try:
            # YOUR CODE HERE - PyMuPDFLoader로 PDF 로딩
            # loader = PyMuPDFLoader(file_path)
            # documents = loader.load()
            # 
            # PyMuPDFLoader: PDF의 각 페이지를 Document 객체로 변환
            # 메타데이터(페이지 번호, 소스 등)도 함께 저장됨
            documents = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
            if not documents:
                return [], "PDF 파일이 비어있습니다."
            
            return documents, f"✅ {len(documents)}개의 페이지를 로드했습니다."
        except Exception as e:
            return [], f"❌ PDF 로딩 실패: {str(e)}"
    
    def split_documents(self, documents: List[Document]) -> Tuple[List[Document], str]:
        """
        문서를 청크로 분할합니다.
        
        Args:
            documents: 원본 문서 리스트
            
        Returns:
            (청크 리스트, 상태 메시지)
        """
        try:
            # YOUR CODE HERE - text_splitter로 문서 분할
            # chunks = self.text_splitter.split_documents(documents)
            # 
            # split_documents(): 문서 리스트를 작은 청크로 분할
            # 각 청크는 독립적으로 검색 가능한 단위가 됨
            chunks = []  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
            if not chunks:
                return [], "문서 분할 결과가 없습니다."
            
            # 청크 통계
            chunk_lengths = [len(chunk.page_content) for chunk in chunks]
            avg_length = sum(chunk_lengths) / len(chunk_lengths)
            
            return chunks, f"✅ {len(chunks)}개의 청크로 분할했습니다. (평균 {int(avg_length)}자)"
        except Exception as e:
            return [], f"❌ 청킹 실패: {str(e)}"
    
    def create_vectorstore(
        self, 
        chunks: List[Document], 
        persist_directory: Optional[str] = None
    ) -> Tuple[Optional[Chroma], str]:
        """
        청크로부터 벡터 스토어를 생성합니다.
        
        Args:
            chunks: 문서 청크 리스트
            persist_directory: 벡터 스토어 저장 경로 (None이면 메모리만)
            
        Returns:
            (벡터 스토어 객체, 상태 메시지)
        """
        try:
            if not chunks:
                return None, "청크가 없습니다."
            
            # YOUR CODE HERE - Chroma 벡터 스토어 생성
            # vectorstore = Chroma.from_documents(
            #     documents=chunks,
            #     embedding=self.embeddings,
            #     persist_directory=persist_directory
            # )
            # 
            # Chroma.from_documents(): 문서를 임베딩하고 벡터 스토어에 저장
            # - documents: 청크 리스트
            # - embedding: 임베딩 모델
            # - persist_directory: 디스크 저장 경로 (None이면 메모리만)
            vectorstore = None  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요
            
            if vectorstore is None:
                return None, "벡터 스토어 생성 실패"
            
            # 저장된 벡터 개수 확인
            count = vectorstore._collection.count()
            
            return vectorstore, f"✅ {count}개의 벡터를 생성하고 저장했습니다."
        except Exception as e:
            return None, f"❌ 벡터 스토어 생성 실패: {str(e)}"
    
    def process_pdf_file(
        self, 
        uploaded_file, 
        persist_directory: Optional[str] = None
    ) -> Tuple[Optional[Chroma], dict]:
        """
        업로드된 PDF 파일을 전체 파이프라인으로 처리합니다.
        
        전체 흐름:
        1. PDF 저장 → 2. 로딩 → 3. 청킹 → 4. 벡터 스토어 생성
        """
        progress = {
            "status": "진행중",
            "current_step": "",
            "steps": {},
            "file_info": {
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "pages": 0,
                "chunks": 0
            }
        }
        
        try:
            # 1단계: 임시 파일로 저장
            progress["current_step"] = "파일 저장"
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # 2단계: PDF 로딩
            progress["current_step"] = "PDF 로딩"
            documents, load_msg = self.load_pdf(tmp_path)
            progress["steps"]["load"] = {
                "message": load_msg,
                "success": len(documents) > 0
            }
            progress["file_info"]["pages"] = len(documents)
            
            if not documents:
                progress["status"] = "실패"
                os.unlink(tmp_path)
                return None, progress
            
            # 3단계: 청킹
            progress["current_step"] = "텍스트 청킹"
            chunks, chunk_msg = self.split_documents(documents)
            progress["steps"]["chunk"] = {
                "message": chunk_msg,
                "success": len(chunks) > 0
            }
            progress["file_info"]["chunks"] = len(chunks)
            
            if not chunks:
                progress["status"] = "실패"
                os.unlink(tmp_path)
                return None, progress
            
            # 4단계: 벡터 스토어 생성
            progress["current_step"] = "임베딩 및 벡터 스토어 생성"
            vectorstore, embed_msg = self.create_vectorstore(chunks, persist_directory)
            progress["steps"]["embed"] = {
                "message": embed_msg,
                "success": vectorstore is not None
            }
            
            # 임시 파일 삭제
            os.unlink(tmp_path)
            
            if vectorstore is None:
                progress["status"] = "실패"
                return None, progress
            
            # 완료
            progress["status"] = "완료"
            progress["current_step"] = "완료"
            
            return vectorstore, progress
            
        except Exception as e:
            progress["status"] = "실패"
            progress["steps"]["error"] = {
                "message": f"❌ 처리 중 오류 발생: {str(e)}",
                "success": False
            }
            return None, progress
    
    def get_retriever(self, vectorstore: Chroma, k: int = 5):
        """
        벡터 스토어로부터 검색기를 생성합니다.
        
        Args:
            vectorstore: Chroma 벡터 스토어
            k: 검색할 문서 개수
            
        Returns:
            검색기 객체
        """
        # YOUR CODE HERE - 벡터 스토어에서 검색기 생성
        # return vectorstore.as_retriever(
        #     search_type="similarity",
        #     search_kwargs={"k": k}
        # )
        # 
        # as_retriever(): 벡터 스토어를 검색기로 변환
        # - search_type="similarity": 유사도 기반 검색
        # - k: 반환할 문서 개수
        pass  # 위의 YOUR CODE HERE를 채우면 이 줄을 삭제하세요

