import uuid
from typing import Any, Dict, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchAny,
    PayloadSchemaType,
)
from sentence_transformers import SentenceTransformer

from app.config import settings


class VectorStoreService:
    """Abstraction over Qdrant used to store and retrieve startup advice chunks."""

    def __init__(self) -> None:
        # Initialize Qdrant client
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY or None,
        )

        # Multilingual embedding model (Arabic + English)
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        # Single collection that stores all advice vectors
        self.collection_name = f"{settings.COLLECTION_PREFIX}_kb"

    def initialize_collection(self) -> None:
        """Create the Qdrant collection if it does not already exist,
        and ensure payload indexes are created.
        """
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            print(f"Created collection: {self.collection_name}")
        else:
            print(f"Collection already exists: {self.collection_name}")

        # Very important: ensure payload indexes for fields we use in filters
        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        """Ensure that payload indexes exist for frequently filtered fields."""
        # Index for 'stage' (used in multi-stage retrieval)
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="stage",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            print("Created payload index on 'stage'.")
        except Exception as e:  # noqa: BLE001
            # Most likely it already exists; we can safely ignore
            print(f"Payload index on 'stage' may already exist: {e}")

        # Optional: index for 'book' if you want to filter by book in the future
        try:
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="book",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            print("Created payload index on 'book'.")
        except Exception as e:  # noqa: BLE001
            print(f"Payload index on 'book' may already exist: {e}")

    def _embed_text(self, text: str) -> List[float]:
        """Generate an embedding vector for a single text string."""
        return self.embedding_model.encode(text).tolist()

    def store_documents(self, documents: List[Any]) -> None:
        """Store a list of LangChain Document objects in Qdrant.

        Each document is expected to have:
        - page_content: the text to embed
        - metadata: a dict containing keys like stage, book, advice_id, etc.
        """
        if not documents:
            print("No documents provided to store.")
            return

        points: List[PointStruct] = []

        for doc in documents:
            text = doc.page_content
            metadata = dict(doc.metadata or {})

            embedding = self._embed_text(text)

            payload: Dict[str, Any] = {"content": text}
            payload.update(metadata)

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload,
            )
            points.append(point)

        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            print(f"Stored {len(points)} documents in {self.collection_name}")
        except Exception as e:  # noqa: BLE001
            print(f"Error storing documents in {self.collection_name}: {e}")

    def search_similar(
        self,
        query: str,
        limit: int = 5,
        stages: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for documents similar to a query string.

        If `stages` is provided, Qdrant will filter by the `stage` payload field
        using a proper payload index.
        """
        if not self.client.collection_exists(self.collection_name):
            print("Collection does not exist; no search performed.")
            return []

        query_embedding = self._embed_text(query)

        qdrant_filter: Optional[Filter] = None
        if stages:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key="stage",
                        match=MatchAny(any=stages),
                    )
                ]
            )

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=qdrant_filter,
                limit=limit,
            )
        except Exception as e:  # noqa: BLE001
            print(f"Error searching in {self.collection_name}: {e}")
            return []

        docs: List[Dict[str, Any]] = []
        for r in results:
            payload = r.payload or {}
            docs.append(
                {
                    "content": payload.get("content", ""),
                    "source": payload.get("book", payload.get("source", "unknown")),
                    "score": r.score,
                    "metadata": payload,
                }
            )

        docs.sort(key=lambda x: x["score"], reverse=True)
        return docs[:limit]

    def get_collection_stats(self) -> Dict[str, Any]:
        """Return basic statistics about the single collection."""
        stats: Dict[str, Any] = {}
        if self.client.collection_exists(self.collection_name):
            try:
                info = self.client.get_collection(self.collection_name)
                stats[self.collection_name] = {
                    "vectors_count": info.vectors_count,
                    "status": info.status,
                }
            except Exception as e:  # noqa: BLE001
                print(f"Error getting stats for {self.collection_name}: {e}")
        return stats
