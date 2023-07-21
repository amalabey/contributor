import semantic_kernel as sk
import json
import logging
from semantic_kernel.connectors.ai.open_ai import (
    AzureTextCompletion,
    OpenAITextCompletion,
)
from semantic_kernel.orchestration.context_variables import ContextVariables

useAzureOpenAI = False


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
    )

    kernel = sk.Kernel()

    # Configure AI service used by the kernel. Load settings from the .env file.
    if useAzureOpenAI:
        deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
        kernel.add_text_completion_service(
            "dv", AzureTextCompletion(deployment, endpoint, api_key)
        )
    else:
        api_key, org_id = sk.openai_settings_from_dot_env()
        kernel.add_text_completion_service(
            "dv", OpenAITextCompletion("text-davinci-003", api_key, org_id)
        )

    skills_directory = "skills"

    reviewer_skill = kernel.import_semantic_skill_from_directory(
        skills_directory, "Reviewer"
    )

    review_function = reviewer_skill["Review"]

    code_block = ""
    with open("tests/data/method-UpdateOrderAsync.cs", "+r") as file:
        code_block = file.read()

    # The "input" variable in the prompt is set by "content" in the ContextVariables object.
    context_variables = ContextVariables(content=code_block, variables={"lang": "C#"})
    result = review_function(variables=context_variables)

    result_text = result.result  # .replace("\n", "")
    feedback = json.loads(result_text, strict=False)
    print(json.dumps(feedback, indent=2))


if __name__ == "__main__":
    main()
