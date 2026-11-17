from app.langchain_rag.documents import load_markdown_documents, print_document


def main():
    documents = load_markdown_documents()
    print("documents counts:", len(documents))
    print_document(documents)

if __name__ == "__main__":
    main()    