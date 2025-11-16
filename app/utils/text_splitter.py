from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class StartupTextSplitter:
    """Wrapper around RecursiveCharacterTextSplitter for startup advice chunks."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50) -> None:
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        )

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """Split a list of LangChain Document objects into smaller chunks."""
        return self.text_splitter.split_documents(documents)

    def split_text(self, text: str, metadata: dict | None = None) -> list[Document]:
        """Split raw text into chunks with optional metadata."""
        if metadata is None:
            metadata = {}
        docs = [Document(page_content=text, metadata=metadata)]
        return self.split_documents(docs)
