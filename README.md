# chat-ops

Slackbot that allows users to automatically release and deploy an application contained within a GitHub repository. When the user enters the name of the application and the semantic-version increment, a GitHub workflow is invoked to create a new tag and release. This then triggers a second workflow which builds a Dockerfile describing the application and finally updates a YAML file that ArgoCD reads from, to deploy the application to a Kubernetes cluster.

## Instructions for Ubuntu 22.04

### Configure ArgoCD on Docker Desktop

Prerequisite: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. Enable Kubernetes in Docker Desktop settings

2. Create a namespace called argocd where all ArgoCD resources will be installed

```console
ruochen@DESKTOP-ABC:~$ kubectl create namespace argocd
```

3. Install ArgoCD resources. Ensure all pods have been created and are running.

```console
ruochen@DESKTOP-ABC:~$ kubectl apply -n argocd -f <https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml>
ruochen@DESKTOP-ABC:~$ kubectl get pods -n argocd
NAME                                                READY   STATUS    RESTARTS       AGE
argocd-application-controller-0                     1/1     Running   1 (3h1m ago)   9d
argocd-applicationset-controller-69c4b965dc-mjg7t   1/1     Running   1 (3h1m ago)   9d
argocd-dex-server-64d856b94c-r2ftf                  1/1     Running   1 (3h1m ago)   9d
argocd-notifications-controller-f7c967bc9-lllwr     1/1     Running   1 (3h1m ago)   9d
argocd-redis-598f75bc69-jxwj4                       1/1     Running   1 (3h1m ago)   9d
argocd-repo-server-df7f747b4-njxlh                  1/1     Running   1 (3h1m ago)   9d
argocd-server-59d9b8cb46-zss4m                      1/1     Running   1 (3h1m ago)   9d
```

4. Port forward to localhost:8080 to access dashboard

```console
ruochen@DESKTOP-ABC:~$ kubectl port-forward svc/argocd-server -n argocd 8080:443
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

5. Get password to access ArgoCD dashboard. It has been stored as a secret and encoded in base64.

```console
ruochen@DESKTOP-ABC:~$ kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

6. Access the ArgoCD dashboard [here](https://localhost:8080). Use the username 'admin' and password obtained in the previous step to log in.

7. Navigate to the "Applications" tab and create a new app in the default namespace. Set the sync policy to "Automatic" and add the appropriate git repository e.g. https://github.com/reiaxu/chat-ops with the corresponding path of the deployment.yaml file which ArgoCD reads from.

### Creating the Slackbot

Prerequisite: a [Slack](https://slack.com/intl/en-gb/downloads/) workspace

1. Create a new App using the [Slack API](https://api.slack.com/apps). Create the App from scratch, give it a name and add the appropriate workspace the App will be in.

2. Configure App permissions in 'Features: OAuth & Permissions'. Under 'Scopes: Bot Token Scopes', add the `chat:write` permission to the bot. This will allow the bot to post messages.

3. 'Install App to Workspace' under 'OAuth & Permissions: OAuth Tokens & Redirect URLs'. Allow the bot to access the workspace with the appropriate permissions. The app can then be found in the 'Apps' section of your Slack workspace. You may choose to add the app to a channel by clicking on its name and selecting 'Add this app to a channel', or you can simply message it directly.

4. Create and activate a new Python virtual environment in the project directory using Python 3.6 or later with

```console
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ python3 -m venv .venv
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ source .venv/bin/activate
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ python3 -m pip install -r requirements.txt
```

5. Store the Slack signing secret (found in 'Basic Information: App credentials') in a new environment variable

```console
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ export SLACK_SIGNING_SECRET=<your-signing-secret>
```

6. Store the Bot User OAuth Token (xoxb token found in 'OAuth & Permissions: OAuth Tokens for Your Workspace') in another environment variable

```console
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
```

7. Store a [newly-created GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with Read access to metadata, and Read and Wrie access to actions and code in another environment variable.

```console
ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ export BOT_GITHUB_PAT=<your-github-pat>
```

8. To host the bot so that your development environment can receive requests, download [ngrok](https://ngrok.com/download) and run

```console
ruochen@DESKTOP-ABC:~$ ngrok http 3000
ngrok
Want to improve ngrok? Take our survey:  <https://ngrok.com/survey>

Session Status          online
Session Expires         1 hour, 59 minutes
Terms of Service        <https://ngrok.com/tos>
Version                 3.1.1
Region                  Europe (eu)
Latency                 33ms
Web Interface           <http://127.0.0.1:4040>
Forwarding              <https://redacted.eu.ngrok.io> -> <http://localhost:3000>
Connections             ttl     opn     rt1     rt5     p50     p90
                        0       0       0.00    0.00    0.00    0.00
```

9. Running the app as follows will initialise the app with the `App` constructor, and start a HTTP server on port 3000.

```console
(.venv) ruochen@DESKTOP-ABC:/mnt/c/Users/ruoch/chat-ops$ python3 app.py
```

10. The slash command `/release [project-name] [release-type: major/minor/patch]` will be used by users to deploy their releases. Create a new slash command in "Features: Slash Commands" and configure its usage accordingly. For the Slackbot to listen to these requests, Bolt for Python listens for all incoming requests at the ```/slack/events``` route. Add the ngrok url that is port-forwarded to localhost:3000 (e.g. `https://redacted.eu.ngrok.io/slack/events` under "Request URL".

11. Install the app to your Slack workspace under "Settings: Install App" and reinstall the app to your workspace.

12. Test the app by adding the Slackbot to a channel and sending `/release [project-name] [release-type]` to the channel. This should trigger the deployment workflow and create a new GitHub release. It should also add a new replica set to the app deployment in ArgoCD.

## References

1. [ArgoCD on Docker Desktop](https://collabnix.com/getting-started-with-argocd-on-docker-desktop/)
2. [Building an app with Bolt for Python](https://api.slack.com/start/building/bolt-python)
