import threading
from flask import Flask, jsonify, request

from azure_devops.actions import review_pull_request
from core.dispatch import TaskDispatcher

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    data = request.get_json()

    # Run PR review in a separate thread
    pull_request_id = data["resource"]["pullRequestId"]
    print(f"Received webhook for pull request {pull_request_id}")
    task_type = f"review_{pull_request_id}"
    thread = threading.Thread(
        target=TaskDispatcher.execute_task,
        args=(task_type, lambda: review_pull_request(pull_request_id)),
    )
    thread.start()

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run()
