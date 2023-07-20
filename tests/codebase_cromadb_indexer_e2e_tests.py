import unittest
from app.indexer.codebase_chromadb_indexer import CodebaseChromadbIndexer
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class TestCodebaseChromadbIndexer(unittest.TestCase):
    def test_when_csharp_repo_given_builds_vector_db(self):
        db_path = ".db"
        indexer = CodebaseChromadbIndexer("../eShopOnWeb", db_path,
                                          ["bin", "obj", ".git", ".vs"],
                                          [".cs", ".cshtml", ".js", ".css", ".md"])
        indexer.index()
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)
        docs = db.similarity_search("AddItemToBasket method")
        assert len(docs) > 0
