import json
from platform_integration.azure_devops.api import AzureDevOpsApi
from platform_integration.base import BaseWebhookSubscriber
from platform_integration.constants import (
    AZURE_DEVOPS_PLATFORM_NAME,
    APP_NAME,
    API_KEY_HEADER,
    PLATFORM_NAME_HEADER,
    APP_NAME_HEADER,
)


class AzureDevOpsWebhookSubscriber(BaseWebhookSubscriber):
    def __init__(self, client: AzureDevOpsApi, org: str, project_name: str):
        self._client = client
        self._org = org
        self._project_name = project_name

    def subscribe(self, base_url: str, api_key: str = None) -> None:
        """Registers webhooks for the given URL."""
        project_id = self._get_project_id()
        existing_subs = self._get_existing_subscriptions()

        # Register webhooks for PR creation and update events
        for event_type in ["git.pullrequest.created", "git.pullrequest.updated"]:
            payload = self._get_subscription_payload(
                project_id, f"{base_url}/pull_request", api_key, event_type
            )
            # Check if subscription already exists and replace if it does
            existing_sub_id = self._existing_subscription_id(existing_subs, event_type)

            if existing_sub_id:
                api_url = f"https://dev.azure.com/{self._org}/_apis/hooks/subscriptions/{existing_sub_id}?api-version=6.1-preview.1"
                self._client.send_api_request(api_url, "PUT", data=payload)
            else:
                api_url = f"https://dev.azure.com/{self._org}/_apis/hooks/subscriptions?api-version=6.1-preview.1"
                self._client.send_api_request(api_url, "POST", data=payload)

    def _existing_subscription_id(self, existing_subs: dict, event_type: str) -> str:
        subs_for_event_type = [
            sub for sub in existing_subs if sub["eventType"] == event_type
        ]
        if subs_for_event_type:
            for sub in subs_for_event_type:
                headers = self._get_headers(sub["consumerInputs"]["httpHeaders"])
                if headers[APP_NAME_HEADER] == APP_NAME:
                    return sub["id"]
        return None

    def _get_headers(self, headers_text: str) -> dict:
        headers = {}
        for line in headers_text.splitlines():
            key, value = line.split(":")
            headers[key] = value.strip()
        return headers

    def _get_project_id(self) -> str:
        api_url = f"https://dev.azure.com/{self._org}/_apis/projects?api-version=6.1-preview.4"
        response = self._client.send_api_request(api_url, "GET")
        projects = response["value"]
        matched_projects = [
            p for p in projects if p["name"].lower() == self._project_name.lower()
        ]
        if len(matched_projects) == 0:
            raise Exception(f"Project {self._project_name} not found")

        return matched_projects[0]["id"]

    def _get_subscription_payload(
        self, project_id: str, webhook_url: str, api_key: str, event_type: str
    ) -> str:
        payload = json.dumps(
            {
                "publisherId": "tfs",
                "eventType": event_type,
                "subscriber": None,
                "resourceVersion": "1.0",
                "consumerId": "webHooks",
                "consumerActionId": "httpRequest",
                "publisherInputs": {
                    "branch": "",
                    "projectId": project_id,
                    "pullrequestCreatedBy": "",
                    "pullrequestReviewersContains": "",
                },
                "consumerInputs": {
                    "acceptUntrustedCerts": "true",
                    "httpHeaders": f"{API_KEY_HEADER}: {api_key}\n{APP_NAME_HEADER}: {APP_NAME}\n{PLATFORM_NAME_HEADER}: {AZURE_DEVOPS_PLATFORM_NAME}",
                    "url": webhook_url,
                },
            }
        )
        return payload

    def _get_existing_subscriptions(self) -> dict:
        api_url = f"https://dev.azure.com/{self._org}/_apis/hooks/subscriptions?api-version=6.1-preview.1"
        response = self._client.send_api_request(api_url, "GET")
        return response["value"]
