import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from azure_devops.pull_requests import (
    AzureDevOpsPullRequestDataProvider,
    AzureDevOpsPullRequestDecoratorService,
)
from core.code_review.changeset import ChangesetProvider
from core.code_review.comments import ReviewCommentProvider
from core.code_review.lang import LanguageDetector
from core.code_review.reviewer import CodeReviwer

from core.code_review.syntax import SyntaxProvider

DEFAULT_TEMPERATURE = 0.0


def review_pull_request(
    pull_request_id: str,
    env_config_file: str = ".env",
    temperature: float = DEFAULT_TEMPERATURE,
):
    load_dotenv(env_config_file)
    model_name = os.getenv("MODEL_NAME")
    deployment_name = os.getenv("DEPLOYMENT_NAME")
    llm_model = AzureChatOpenAI(
        model_name=model_name,
        deployment_name=deployment_name,
        temperature=temperature,
    )
    syntax_provider = SyntaxProvider(llm_model, verbose=True)
    changeset_provider = ChangesetProvider()
    review_provider = ReviewCommentProvider(llm_model, verbose=True)
    lang_detector = LanguageDetector()

    org = os.getenv("AZURE_DEVOPS_ORG")
    project = os.getenv("AZURE_DEVOPS_PROJECT")
    pr_data_provider = AzureDevOpsPullRequestDataProvider(org, project)
    pr_decorator_svc = AzureDevOpsPullRequestDecoratorService(org, project)

    code_reviewer = CodeReviwer(
        pr_data_provider,
        pr_decorator_svc,
        changeset_provider,
        syntax_provider,
        lang_detector,
        review_provider,
    )
    code_reviewer.review_pull_request(pull_request_id)
