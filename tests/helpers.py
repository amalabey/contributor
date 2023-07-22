import os
from typing import Optional, Tuple
from dotenv import dotenv_values
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)

script_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(script_path)

USE_AZURE_OPENAI = True
ENV_FILE_PATH = os.path.join(parent_directory, "..", ".env")


def openai_settings_from_dot_env(
    env_file_path: str = None,
) -> Tuple[str, Optional[str]]:
    config = dotenv_values(env_file_path or ".env")
    api_key = config.get("OPENAI_API_KEY", None)
    org_id = config.get("OPENAI_ORG_ID", None)

    assert api_key is not None, "OpenAI API key not found in .env file"

    # It's okay if the org ID is not found (not required)
    return api_key, org_id


def azure_openai_settings_from_dot_env(
    env_file_path: str = None, include_deployment=True
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


def get_kernel():
    kernel = sk.Kernel()
    if USE_AZURE_OPENAI:
        deployment, api_key, endpoint = azure_openai_settings_from_dot_env(
            env_file_path=ENV_FILE_PATH
        )
        kernel.add_text_completion_service(
            "dv",
            AzureChatCompletion(deployment, endpoint, api_key),
        )
    else:
        api_key, org_id = openai_settings_from_dot_env(env_file_path=ENV_FILE_PATH)
        kernel.add_text_completion_service(
            "dv",
            OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id),
        )

    return kernel


def get_skill(kernel: sk.Kernel, skill_name: str):
    skills_directory = "skills"
    skill = kernel.import_semantic_skill_from_directory(skills_directory, skill_name)
    return skill
