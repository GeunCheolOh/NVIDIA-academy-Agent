"""
setup_d2l.py - D2L 교재 다운로드 및 벡터 스토어 구축
======================================================

목적:
    D2L (Dive into Deep Learning) 교재 PDF를 다운로드하고
    벡터 스토어를 구축하여 재사용 가능하게 만듭니다.

사용:
    python setup_d2l.py
"""

import os
import requests
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# 설정
PDF_URL = "https://d2l.ai/d2l-en.pdf"
PDF_PATH = "d2l-en.pdf"
CHROMA_DB_PATH = "./chroma_db_d2l"
MAX_PAGES = 100  # 처음 100페이지만 처리 (전체는 너무 오래 걸림)


def download_pdf(url: str, path: str) -> bool:
    """
    PDF 파일을 다운로드합니다.
    
    Args:
        url: PDF URL
        path: 저장 경로
        
    Returns:
        성공 여부
    """
    if Path(path).exists():
        print(f"✅ PDF 파일이 이미 존재합니다: {path}")
        return True
    
    try:
        print(f"📥 PDF 다운로드 중: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                # 진행률 표시
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\r진행: {progress:.1f}%", end='')
        
        print(f"\n✅ PDF 다운로드 완료: {path}")
        return True
        
    except Exception as e:
        print(f"❌ PDF 다운로드 실패: {str(e)}")
        return False


def setup_vectorstore(
    pdf_path: str,
    chroma_path: str,
    max_pages: int = None
) -> Chroma:
    """
    PDF로부터 벡터 스토어를 구축합니다.
    
    Args:
        pdf_path: PDF 파일 경로
        chroma_path: Chroma DB 저장 경로
        max_pages: 처리할 최대 페이지 수
        
    Returns:
        Chroma 벡터 스토어 객체
    """
    # 이미 벡터 스토어가 있으면 로드
    if Path(chroma_path).exists():
        print(f"✅ 기존 벡터 스토어를 로드합니다: {chroma_path}")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        vectorstore = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )
        count = vectorstore._collection.count()
        print(f"✅ {count}개의 벡터가 로드되었습니다.")
        return vectorstore
    
    print(f"🔨 새로운 벡터 스토어를 생성합니다...")
    
    # 1. PDF 로딩
    print(f"📖 PDF 로딩 중: {pdf_path}")
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    
    if max_pages:
        documents = documents[:max_pages]
        print(f"✅ {len(documents)}개 페이지 로드 (최대 {max_pages}페이지)")
    else:
        print(f"✅ {len(documents)}개 페이지 로드")
    
    # 2. 텍스트 청킹
    print("✂️  텍스트 청킹 중...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ {len(chunks)}개의 청크 생성")
    
    # 3. 임베딩 및 벡터 스토어 생성
    print("🔢 임베딩 생성 및 벡터 스토어 구축 중...")
    print("   (이 작업은 몇 분 정도 소요될 수 있습니다)")
    
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )
    
    count = vectorstore._collection.count()
    print(f"✅ 벡터 스토어 생성 완료: {count}개 벡터")
    
    return vectorstore


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("D2L 교재 벡터 스토어 설정")
    print("=" * 60)
    
    # 1. PDF 다운로드
    if not download_pdf(PDF_URL, PDF_PATH):
        print("❌ 설정 실패")
        return
    
    # 2. 벡터 스토어 구축
    try:
        vectorstore = setup_vectorstore(
            PDF_PATH,
            CHROMA_DB_PATH,
            MAX_PAGES
        )
        
        # 3. 테스트 검색
        print("\n" + "=" * 60)
        print("테스트 검색")
        print("=" * 60)
        
        test_query = "What is deep learning?"
        print(f"질문: {test_query}")
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(test_query)
        
        print(f"\n검색 결과 ({len(docs)}개 문서):")
        for i, doc in enumerate(docs, 1):
            print(f"\n[문서 {i}]")
            print(doc.page_content[:200] + "...")
        
        print("\n" + "=" * 60)
        print("✅ 설정 완료!")
        print("=" * 60)
        print(f"벡터 스토어 위치: {CHROMA_DB_PATH}")
        print("이제 app_router.py를 실행할 수 있습니다.")
        
    except Exception as e:
        print(f"❌ 벡터 스토어 생성 실패: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

