import logging
from typing import List
from app.indexer.codebase_indexer import CodebaseIndexer
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

logger = logging.getLogger(__name__)


class CodebaseChromadbIndexer(CodebaseIndexer):
    def __init__(self, codebase_path: str,
                 db_path: str,
                 exclusions: List[str] = None,
                 included_extensions: List[str] = None):
        super().__init__()
        self.codebase_path = codebase_path
        self.db_path = db_path
        self.exclusions = exclusions
        self.included_extensions = included_extensions

    def index(self):
        # Read each code file and add it to the corpus
        docs = []
        for file_path in self.get_repo_files(self.codebase_path,
                                             self.exclusions,
                                             self.included_extensions):
            logger.info(f"Loading file {file_path}")
            try:
                loader = TextLoader(file_path, encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception as e:
                logger.error(f"Error loading file {file_path}: {e}")

        # Use embeddings
        embeddings = OpenAIEmbeddings()

        # Store in Vector store (Chroma)
        db = Chroma.from_documents(docs, embeddings,
                                   persist_directory=self.db_path)
        db.persist()
        logger.info(f"Persisting ChromaDB to {self.db_path}")
