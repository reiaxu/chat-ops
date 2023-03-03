# chat-ops

## Instructions

### Configure ArgoCD on Docker Desktop with Ubuntu 22.04

Prerequisite: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

1. Enable Kubernetes in Docker Desktop settings
2. Create a namespace called argocd where all ArgoCD resources will be installed

```
ruochen@DESKTOP-ABC:~$ kubectl create namespace argocd
```

3. Install ArgoCD resources. Ensure all pods have been created and are running.

```
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

```
ruochen@DESKTOP-ABC:~$ kubectl port-forward svc/argocd-server -n argocd 8080:443
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

5. Get password to access ArgoCD dashboard. It has been stored as a secret and encoded in base64.

```
ruochen@DESKTOP-ABC:~$ kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

6. Access the ArgoCD dashboard [here](https://localhost:8080). Use the username 'admin' and password obtained in the previous step to log in.

7. Create ArgoCD application that points to deployment

### Creating the Slackbot in Windows

Prerequisite: a [Slack](https://slack.com/intl/en-gb/downloads/) workspace

1. Create a new App using the [Slack API](https://api.slack.com/apps). Create the App from scratch, give it a name and add the appropriate workspace the App will be in.
2. Configure App permissions in 'Features: OAuth & Permissions'. Under 'Scopes: Bot Token Scopes', add the ```chat:write``` permission to the bot. This will allow the bot to post messages.
3. 'Install App to Workspace' under 'OAuth & Permissions: OAuth Tokens & Redirect URLs'. Allow the bot to access the workspace with the appropriate permissions. The app can then be found in the 'Apps' section of your Slack workspace. You may choose to add the app to a channel by clicking on its name and selecting 'Add this app to a channel', or you can simply message it directly.
4. Create and activate a new Python virtual environment in the project directory using Python 3.6 or later with

```
PS C:\Users\ruoch\chat-ops> python3 -m venv .venv
PS C:\Users\ruoch\chat-ops> .\.venv\Scripts\activate
```

5. Store the Slack signing secret (found in 'Basic Information: App credentials') in a new environment variable

```
(.venv) PS C:\Users\ruoch\chat-ops> set SLACK_SIGNING_SECRET=\<your-signing-secret>
```

6. Store the Bot User OAuth Token (xoxb token found in 'OAuth & Permissions: OAuth Tokens for Your Workspace') in another environment variable

```
(.venv) PS C:\Users\ruoch\chat-ops> set SLACK_BOT_TOKEN=xoxb-\<your-bot-token>
```

7. Store a [newly-created GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with Read access to metadata, and Read and Wrie access to actions and code in another environment variable.

```
(.venv) PS C:\Users\ruoch\chat-ops> set BOT_GITHUB_PAT=<your-github-pat>
```

8. Install the '''slack_bolt''' Python package to your virtual environment

```
(.venv) PS C:\Users\ruoch\chat-ops> pip install slack_bolt
```

9. To host the bot so that your development environment can receive requests, download [ngrok](https://ngrok.com/download) and run

```
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

10.  

## References

1. [ArgoCD on Docker Desktop](https://collabnix.com/getting-started-with-argocd-on-docker-desktop/)
