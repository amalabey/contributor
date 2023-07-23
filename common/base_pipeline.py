from abc import ABC, abstractmethod
from typing import Optional, Tuple
from dotenv import dotenv_values
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"


class BasePipeline(ABC):
    def __init__(
        self, use_azure_openai: bool = True, env_file_path: str = ".env"
    ) -> None:
        super().__init__()
        self.use_azure_openai = use_azure_openai
        self.env_file_path = env_file_path

    @abstractmethod
    def execute(self, source: str, target: str):
        pass

    def get_kernel(self) -> sk.Kernel:
        kernel = sk.Kernel()
        if self.use_azure_openai:
            deployment, api_key, endpoint = self._azure_openai_settings_from_dot_env(
                self.env_file_path
            )
            kernel.add_text_completion_service(
                "dv",
                AzureChatCompletion(deployment, endpoint, api_key),
            )
        else:
            api_key, org_id = self._openai_settings_from_dot_env(
                env_file_path=self.env_file_path
            )
            kernel.add_text_completion_service(
                "dv",
                OpenAIChatCompletion(DEFAULT_OPENAI_MODEL, api_key, org_id),
            )

        return kernel

    def _openai_settings_from_dot_env(
        self,
        env_file_path: str = None,
    ) -> Tuple[str, Optional[str]]:
        config = dotenv_values(env_file_path or ".env")
        api_key = config.get("OPENAI_API_KEY", None)
        org_id = config.get("OPENAI_ORG_ID", None)

        assert api_key is not None, "OpenAI API key not found in .env file"

        # It's okay if the org ID is not found (not required)
        return api_key, org_id

    def _azure_openai_settings_from_dot_env(
        self, env_file_path: str = None, include_deployment=True
    ) -> Tuple[str, str, str]:
        deployment, api_key, endpoint = None, None, None
        config = dotenv_values(env_file_path or ".env")
        deployment = config.get("AZURE_OPENAI_DEPLOYMENT_NAME", None)
        api_key = config.get("AZURE_OPENAI_API_KEY", None)
        endpoint = config.get("AZURE_OPENAI_ENDPOINT", None)

        # Azure requires the deployment name, the API key and the endpoint URL.
        if include_deployment:
            assert (
                deployment is not None
            ), "Azure OpenAI deployment name not found in .env file"

        assert api_key is not None, "Azure OpenAI API key not found in .env file"
        assert endpoint is not None, "Azure OpenAI endpoint not found in .env file"

        return deployment or "", api_key, endpoint
