import typing as t

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from google import genai
from google.api_core import retry
from google.genai import types
from google.genai.errors import APIError

from .._singleton import _SingletonMeta
from ..configs import config
from ..settings import Settings

client = genai.Client()


# Define a helper to retry when per-minute quota is reached.
def is_retriable(e):
    return isinstance(e, APIError) and e.code in {429, 503}


class GeminiEmbeddingFunction(EmbeddingFunction, metaclass=_SingletonMeta):
    # Specify whether to generate embeddings for documents, or queries
    EMBEDDING_MODEL = config.embedding_model
    OUTPUT_DIM = config.embedding_output_dim

    def __init__(
        self,
        document_mode: bool = True,
        embedding_model: str | None = None,
        output_dim: int | None = None,
    ):
        self.document_mode = document_mode
        self.embedding_model = embedding_model
        self.output_dim = output_dim

    @property
    def task_type(self) -> str:
        return "RETRIEVAL_DOCUMENT" if self.document_mode else "RETRIEVAL_QUERY"

    @retry.Retry(predicate=is_retriable)
    @t.override
    def __call__(self, input: Documents) -> Embeddings:
        response = client.models.embed_content(
            model=self.embedding_model or self.EMBEDDING_MODEL,
            contents=input,  # type: ignore
            config=types.EmbedContentConfig(
                task_type=self.task_type,
                output_dimensionality=self.output_dim or self.OUTPUT_DIM,
            ),
        )
        return [e.values for e in response.embeddings]  # type: ignore


def get_db(collection_name: str | None = None) -> chromadb.Collection:
    """Get or create a ChromaDB collection.

    Args:
        collection_name (str | None): The name of the collection. If None,
            a default name will be used.
    Returns:
        chromadb.Collection: The ChromaDB collection instance.
    """
    if collection_name is None:
        json_resume_path = Settings().json_resume.path
        collection_name = json_resume_path.stem

    chromadb_dir = Settings().chromadb.persist_dir

    chroma_client = chromadb.PersistentClient(path=chromadb_dir)
    db = chroma_client.get_or_create_collection(
        name=collection_name,
        embedding_function=GeminiEmbeddingFunction(document_mode=True),
    )
    return db


ValidExperienceKeys = t.Literal[
    "work",
    "volunteer",
    "certificates",
    "projects",
    "skills",
    "interests",
]


class ExperienceRetrieval(t.TypedDict):
    exp_id: str
    exp_type: ValidExperienceKeys
    description: str
    distance: float


class ExperienceRetrievalResult(t.TypedDict, total=False):
    status: str
    retrieved_experiences: list[ExperienceRetrieval]
    message: str


# Global database instance (to be initialized)
db: chromadb.Collection | None = None
embed_fn: GeminiEmbeddingFunction | None = None


def init_db(json_resume_file_stem: str):
    global db, embed_fn  # noqa: PLW0603
    embed_fn = GeminiEmbeddingFunction(document_mode=True)
    db_name = "cv_embeddings_" + json_resume_file_stem
    chroma_client = chromadb.Client()
    db = chroma_client.get_or_create_collection(
        name=db_name, embedding_function=embed_fn
    )


def get_all_experience_types() -> dict[str, list[str] | str]:
    """Get all unique experience types stored in the ChromaDB.

    Returns:
        dict[str, list[str] | str]: A dictionary containing the status and either a list of unique experience types or an error message.
    """
    if db is None or db.count() == 0:
        return {
            "status": "error",
            "message": "The database is empty.",
        }

    try:
        # Query the database for all unique experience types.
        result = db.get(include=["metadatas"])

        metadatas = []
        if result["metadatas"]:
            metadatas = result["metadatas"]

        experience_types: set[str] = set()
        for metadata in metadatas:
            item_type = t.cast(str, metadata.get("item_type"))
            if item_type:
                experience_types.add(item_type)

        return {
            "status": "success",
            "experience_types": list(experience_types),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


def count_experiences_by_type(
    exp_type: ValidExperienceKeys,
) -> dict[str, int | str]:
    """Count the number of experiences in the ChromaDB for a specific type.

    Args:
        exp_type (ValidExperienceKeys): The type of experience to count.
    Returns:
        int: The number of experiences of the specified type in the database.
    """
    if db is None or db.count() == 0:
        return {
            "status": "error",
            "message": "The database is empty.",
        }

    try:
        # Query the database for the count of experiences of the specified type.
        result = db.get(where={"item_type": exp_type})

        ids = result["ids"]

        return {
            "status": "success",
            "count": len(ids),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


def retrieve_experiences_by_query(
    query: str,
    exp_type: ValidExperienceKeys | t.Literal["all"],
    n_results: int,
) -> ExperienceRetrievalResult:
    """Retrieve experiences from the ChromaDB based on a query string.
    The embedding function will be switched to query mode during this operation.

    Args:
        query (str): The query string to search for.
        n_results (int): The number of top results to retrieve. If the value
            is less than or equal to zero, all experiences will be retrieved.

    Returns:
        dict[str, str]: A dictionary containing the status and retrieved experiences.

    Example:
        >>> retrieve_experiences_by_query(
        ...     query="Python, SQL, Machine Learning",
        ...     n_results=2,
        ... )
        {
            "status": "success",
            "retrieved_experiences": [
                {
                    "exp_id": "work_1",
                    "description": "Developed data pipelines using Python and SQL...",
                    "exp_type": "work",
                    "distance": 0.12345
                },
                {
                    "exp_id": "project_3",
                    "description": "Implemented machine learning models using Python...",
                    "exp_type": "project",
                    "distance": 0.23456
                }
            ]
        }
    """
    if embed_fn is None or db is None:
        return {
            "status": "error",
            "message": "Database not initialized. Call init_db() first.",
        }

    # Switch to query mode when generating embeddings.
    embed_fn.document_mode = False

    if db.count() == 0:
        return {
            "status": "error",
            "message": "The database is empty. No experiences to retrieve.",
        }

    # Search the Chroma DB using the specified query.
    if n_results <= 0:
        n_results = db.count()

    try:
        where = {"item_type": exp_type} if exp_type != "all" else None
        result = db.query(
            query_texts=[query],
            n_results=n_results,
            where=where,  # type: ignore
        )

        documents: list[str] = []
        ids: list[str] = []
        metadatas: list[dict] = []
        distances: list[float] = []

        if result["documents"]:
            documents = result["documents"][0]

        if result["ids"]:
            ids = result["ids"][0]

        if result["metadatas"]:
            metadatas = result["metadatas"][0]  # type: ignore

        if result["distances"]:
            distances = result["distances"][0]

        retrived_experiences = [
            ExperienceRetrieval(
                exp_type=t.cast(ValidExperienceKeys, str(metadata["item_type"])),
                description=passage,
                exp_id=exp_id,
                distance=distance,
            )
            for exp_id, passage, metadata, distance in zip(
                ids, documents, metadatas, distances, strict=False
            )
        ]

        return {
            "status": "success",
            "retrieved_experiences": retrived_experiences,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


def ingest_resume(json_resume: t.Any) -> dict[str, str]:
    """Ingest a JSON resume into the ChromaDB.

    Args:
        json_resume (JsonResume): The JSON resume object to ingest.

    Returns:
        dict[str, str]: A dictionary containing the status of the operation.
    """
    if db is None or embed_fn is None:
        return {
            "status": "error",
            "message": "Database not initialized. Call init_db() first.",
        }

    # Switch to document mode when generating embeddings.
    embed_fn.document_mode = True

    documents: list[str] = []
    ids: list[str] = []
    metadatas: list[dict[str, t.Any]] = []

    # Helper to add items
    def add_items(
        items: list[t.Any] | None,
        item_type: str,
        id_prefix: str,
        text_field: str = "summary",
    ):
        if not items:
            return
        for i, item in enumerate(items):
            item_dict = item.model_dump() if hasattr(item, "model_dump") else item
            text = item_dict.get(text_field)
            if not text and item_type == "skills":
                # For skills, we might want to join keywords if name is not enough or use name
                text = (
                    f"{item_dict.get('name', '')}:"
                    f" {', '.join(item_dict.get('keywords', []))}"
                )

            if text:
                documents.append(text)
                ids.append(f"{id_prefix}_{i}")
                metadatas.append({"item_type": item_type})

    # Work
    add_items(json_resume.work, "work", "work")
    # Volunteer
    add_items(json_resume.volunteer, "volunteer", "volunteer")
    # Projects
    add_items(json_resume.projects, "projects", "projects")
    # Certificates
    add_items(json_resume.certificates, "certificates", "certificates")
    # Skills
    add_items(json_resume.skills, "skills", "skills")
    # Interests
    add_items(json_resume.interests, "interests", "interests")

    if not documents:
        return {
            "status": "warning",
            "message": "No experiences found to ingest.",
        }

    try:
        db.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas,  # type: ignore
        )
        return {
            "status": "success",
            "message": f"Successfully ingested {len(documents)} items.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
