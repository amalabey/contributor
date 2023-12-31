import os
import sys
from dotenv import load_dotenv
from platform_integration.azure_devops.subscribe import AzureDevOpsWebhookSubscriber
from platform_integration.azure_devops.api import AzureDevOpsApi
from platform_integration.constants import API_KEY_CONFIG_KEY


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1 and args[0] == "register":
        base_url = args[1]
        if not base_url:
            raise Exception("Webhook URL must be provided as an argument")

        # load env variables from .env if it exists
        if os.path.exists(".env"):
            load_dotenv(".env")

        org = os.getenv("AZURE_DEVOPS_ORG")
        if not org:
            raise Exception("AZURE_DEVOPS_ORG environment variable must be set")

        project_name = os.getenv("AZURE_DEVOPS_PROJECT")
        if not project_name:
            raise Exception("AZURE_DEVOPS_PROJECT environment variable must be set")

        webhook_api_key = os.getenv(API_KEY_CONFIG_KEY)
        client = AzureDevOpsApi()
        subscriber = AzureDevOpsWebhookSubscriber(client, org, project_name)
        subscriber.subscribe(base_url, webhook_api_key)
    else:
        print("Unknown command")
