import os
from langchain.chat_models import AzureChatOpenAI
from langchain.llms.base import BaseLLM
from dotenv import load_dotenv

DEFAULT_TEMPERATURE = 0.0


class ModelBuilder:
    def __init__(self):
        pass

    def with_azure_chat_open_ai(
        self,
        env_config_file: str = "../.env",
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> "ModelBuilder":
        load_dotenv(env_config_file)
        model_name = os.getenv("MODEL_NAME")
        deployment_name = os.getenv("DEPLOYMENT_NAME")
        self._llm_model = AzureChatOpenAI(
            model_name=model_name,
            deployment_name=deployment_name,
            temperature=temperature,
        )
        return self

    def build(self) -> BaseLLM:
        return self._llm_model
