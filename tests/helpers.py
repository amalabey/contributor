import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.llms.base import BaseLLM

DEFAULT_TEMPERATURE = 0.0


def get_model(temperature: float = DEFAULT_TEMPERATURE) -> BaseLLM:
    load_dotenv("../.env")
    model_name = os.getenv("MODEL_NAME")
    deployment_name = os.getenv("DEPLOYMENT_NAME")
    llm = AzureChatOpenAI(
        model_name=model_name, deployment_name=deployment_name, temperature=temperature
    )
    return llm
