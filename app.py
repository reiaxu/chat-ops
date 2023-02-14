import os
import requests
import json
# Use the package we installed
from slack_bolt import App

username = "reiaxu"
workflow_id = 48266115
workflow_ref = "main"
github_token = os.environ.get("BOT_GITHUB_PAT")

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# /release [project name] [major/minor/patch]
@app.command("/release")
def trigger_workflow(ack, body, respond):
    # Acknowledge command request
    ack()

    proj_name = body['text'].split(" ")[0]
    release_type = body['text'].split(" ")[1]
    respond(f"Creating a " + release_type + " release for " + proj_name + " project...")

    if release_type == "major" or release_type == "minor" or release_type == "patch":
        response = requests.post( 
            f"https://api.github.com/repos/{username}/{proj_name}/actions/workflows/{workflow_id}/dispatches",
            headers={"Authorization": f"Bearer {github_token}"},
            json={"ref": workflow_ref, "inputs": {"patchtype": release_type}}
        )
        if response.status_code >= 400:
            raise ValueError(f"Failed to trigger workflow: {response.status_code} {response.text}")
        respond(f"Released...")
    else:
        respond(f"Make sure release type is either major, minor or patch!")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))