import os
from langchain.chains.base import Chain
from langchain import PromptTemplate
from langchain.llms.base import BaseLLM
from app.common import PluggableConversationalRetrievalChain
from app.reviewer.model import ReviewCommentCollection
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


class CodeReviewChain:
    """Reviews a given code block and provides a list of comments"""
    @classmethod
    def from_llm(cls, llm: BaseLLM, db_path: str, verbose: bool = True) -> Chain:
        script_path = os.path.abspath(__file__)
        parent_directory = os.path.dirname(script_path)
        prompt_abs_path = os.path.join(parent_directory, "prompts", "review.txt")

        prompt = PromptTemplate.from_file(prompt_abs_path, ["input", "lang", "context"])
        llm_chain = create_structured_output_chain(ReviewCommentCollection,
                                                   llm,
                                                   prompt,
                                                   verbose=verbose)
        combine_docs_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_variable_name="context",
            verbose=verbose
        )

        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)
        retriever = db.as_retriever()
        return PluggableConversationalRetrievalChain.from_llm(llm,
                                                              retriever=retriever,
                                                              combine_docs_chain=combine_docs_chain,
                                                              verbose=True)
