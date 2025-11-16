import os
import sys
import re
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.schema import Document

# Fix Python path when running inside Docker / module mode
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.chat import router as chat_router  # noqa: E402
from app.api.multimodal import router as multimodal_router  # noqa: E402
from app.config import settings  # noqa: E402
from app.services.vector_store import VectorStoreService  # noqa: E402
from app.utils.text_splitter import StartupTextSplitter  # noqa: E402


app = FastAPI(
    title="Startup Advisor AI",
    description="AI-powered startup advisory system based on curated startup knowledge.",
    version="1.0.0",
)

# CORS configuration (can be restricted later as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared services used during startup ingestion
text_splitter = StartupTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)
vector_service = VectorStoreService()


def parse_markdown_advices(md_text: str, base_metadata: dict) -> List[Document]:
    """Parse a markdown file into individual advice documents.

    Each advice block is expected to start with a heading like:

        ## advice_1
        **stage:** Idea
        **topic:** customer_interviews
        ...

    If no such headings are found, the whole file is treated as a single document.
    """
    pattern = re.compile(
        r"(##\s+advice[^\n]*)([\s\S]*?)(?=^##\s+advice|\Z)",
        re.MULTILINE,
    )
    matches = pattern.findall(md_text)

    documents: List[Document] = []

    if not matches:
        # Treat the entire file as one document
        documents.append(
            Document(
                page_content=md_text.strip(),
                metadata=base_metadata,
            )
        )
        return documents

    for header, body in matches:
        header_text = header.strip("#").strip()
        advice_id = header_text

        block_text = f"{header}\n{body}".strip()

        metadata = dict(base_metadata)
        metadata["advice_id"] = advice_id

        # Optional: parse fields from inside the block, if present
        stage_match = re.search(r"\*\*stage:\*\*\s*(.+)", body)
        topic_match = re.search(r"\*\*topic:\*\*\s*(.+)", body)
        complexity_match = re.search(r"\*\*complexity:\*\*\s*(.+)", body)
        tags_match = re.search(r"\*\*tags:\*\*\s*\[(.+)\]", body)

        if stage_match:
            metadata["stage_label"] = stage_match.group(1).strip()
        if topic_match:
            metadata["topic"] = topic_match.group(1).strip()
        if complexity_match:
            metadata["complexity"] = complexity_match.group(1).strip()
        if tags_match:
            raw_tags = tags_match.group(1)
            tags = [
                t.strip().strip('"').strip("'")
                for t in raw_tags.split(",")
                if t.strip()
            ]
            metadata["tags"] = tags

        documents.append(
            Document(
                page_content=block_text,
                metadata=metadata,
            )
        )

    return documents


def ingest_markdown_dataset() -> None:
    """Walk the data directory, parse all .md files, and store them in Qdrant."""
    base_dir = settings.DATA_DIR

    if not os.path.isdir(base_dir):
        print(f"Data directory not found: {base_dir}")
        return

    all_documents: List[Document] = []

    for root, _, files in os.walk(base_dir):
        for filename in files:
            if not filename.lower().endswith(".md"):
                continue

            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, base_dir)
            parts = relative_path.split(os.sep)

            # Stage is the first folder under data, e.g. "01_Ideation_Stage"
            stage = parts[0] if len(parts) >= 2 else "General"
            book_name = os.path.splitext(os.path.basename(filename))[0]

            with open(file_path, "r", encoding="utf-8") as f:
                md_text = f.read()

            base_metadata = {
                "stage": stage,
                "book": book_name,
                "path": file_path,
            }

            docs = parse_markdown_advices(md_text, base_metadata)
            all_documents.extend(docs)

            print(f"Parsed {len(docs)} advice blocks from {file_path}")

    if not all_documents:
        print("No markdown documents found; nothing to ingest.")
        return

    # Split into smaller chunks for embedding
    chunked_docs = text_splitter.split_documents(all_documents)
    print(f"Total chunks after splitting: {len(chunked_docs)}")

    # Ensure collection exists and store vectors
    vector_service.initialize_collection()
    vector_service.store_documents(chunked_docs)
    print("Markdown dataset successfully ingested into Qdrant.")


@app.on_event("startup")
async def on_startup() -> None:
    print("Starting Startup Advisor AI backend...")

    if os.getenv("INGEST_ON_STARTUP", "true").lower() == "true":
        print("INGEST_ON_STARTUP=true → ingesting markdown dataset...")
        ingest_markdown_dataset()
    else:
        print("INGEST_ON_STARTUP=false → skipping ingestion.")

    print("Startup Advisor AI backend is ready.")


@app.get("/")
async def root() -> dict:
    """Simple root endpoint for quick sanity checks."""
    return {
        "message": "Startup Advisor AI backend is running.",
        "docs_url": "/docs",
    }


# Mount routes
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])
app.include_router(multimodal_router, prefix="/api/v1", tags=["multimodal"])
