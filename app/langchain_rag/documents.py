from pathlib import Path
from langchain_core.documents import Document
KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")

def load_markdown_documents(
    base_dir: Path = KNOWLEDGE_BASE_DIR
):
    documents: list[Document] = []
    for file_path in sorted(base_dir.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")
        document_id = file_path.stem
        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "document_id": document_id,
                    "file_title": "markdown"
                }
            )
        )
    return documents
def print_document(documents: list[Document]):
    for index, doc in enumerate(documents, start=1):
        print(f"Document {index}")
        print("metadata:", doc.metadata)
        print("content preview:", doc.page_content[:120])
        print("=" * 80)