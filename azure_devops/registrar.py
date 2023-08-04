from azure_devops.api import ApiClient


class WebhookRegistrar(object):
    def __init__(self, client: ApiClient):
        self._client = client

    """Register a webhook for a given project and repo.

        :param project: The project name.
        :param repo: The repo name.
        :param url: The url to register the webhook to.
        """

    def register_webhook(self, project: str, repo: str, url: str):
        data = {
            "name": "web",
            "url": url,
            "events": ["push"],
            "contentType": "json",
        }
        url = f"{self._client.base_url}/{project}/_apis/git/repositories/{repo}/hooks"
        self._client.send_api_request(url, method="POST", data=data)
