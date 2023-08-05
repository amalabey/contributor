import os
import threading
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from platform_integration.actions import review_pull_request
from core.dispatch import TaskDispatcher
from platform_integration.constants import AZURE_DEVOPS_PLATFORM_NAME

app = Flask(__name__)


@app.route("/pull_request", methods=["POST"])
def handle_webhook():
    data = request.get_json()

    # Validate API key if it is set
    expected_api_key = os.getenv("WEBHOOK_API_KEY")
    if expected_api_key is not None:
        api_key = request.headers.get("X-Api-Key")
        if api_key != expected_api_key:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403

    # Run PR review in a separate thread
    platform = request.headers.get("X-Platform")
    if platform == AZURE_DEVOPS_PLATFORM_NAME:
        pull_request_id = data["resource"]["pullRequestId"]
        print(
            f"Received webhook for pull request {pull_request_id}:  {AZURE_DEVOPS_PLATFORM_NAME}"
        )
        task_type = f"review_{pull_request_id}"
        thread = threading.Thread(
            target=TaskDispatcher.execute_task,
            args=(
                task_type,
                lambda: review_pull_request(
                    pull_request_id, platform=AZURE_DEVOPS_PLATFORM_NAME
                ),
            ),
        )
        thread.start()
    else:
        print(f"Received webhook for unsupported platform: {platform}")
        return jsonify({"message": "Unsupported platform"}), 404

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    load_dotenv(".env")
    app.run()
