# TODO Management LineBot Application

##### Tech blog about this project is [here](https://kk1110.netlify.app/posts/linebot)

## Overview

- TODO Management Application with LineBot
- If you type completed taskname, the task will be deleted.
- To delete all your task, please type "クリア" or "clear"

## Techs

| Tech       | Version  |
| ---------- | -------- |
| Python     | 3.9.7    |
| Flask      | 1.1.4    |
| Kubernetes | 1.23.5   |
| Docker     | 20.10.12 |
| Nginx      | 1.21.6   |
| Mysql      | 5.7      |

## System Architecture

Made by [Draw.io](https://app.diagrams.net/)
![](architecture_linebot.drawio.svg)

## How to run with docker-compose

- You can run this application on your local with docker-compose.
- Note: Running on local cannot prepare SSL configuration, so you cannot set localhost to linebot's callback method. You can just check how this app works.

```
$ pwd
/path/to/dir/linebot/
# Build & Run containers
$ docker-compose up
# Stop & Delete containers
$ docker-compose down --rmi all --volumes --remove-orphans
```

### How to run on GKE

```

# Create your artifacts repositories on GCP.
$ gcloud artifacts repositories create linebot-repo \
    --project=gcp-compute-engine-343613 \
    --repository-format=docker \
    --location=asia-northeast1 \
    --description="Docker repository"

# Create your own cluster.
$ gcloud container clusters create linebot-gke --num-nodes 3 --zone asia-northeast1

# Build image and deploy
$ pwd
/path/to/dir/linebot/
# Flask App image build and push
$ gcloud builds submit \
    --tag asia-northeast1-docker.pkg.dev/gcp-compute-engine-343613/linebot-repo/app-server:1.0.0 ./app/
# Nginx container image build and push
$ gcloud builds submit \
    --tag asia-northeast1-docker.pkg.dev/gcp-compute-engine-343613/linebot-repo/linebot-nginx:1.0.0 ./web/

# Apply each k8s objects
# Build & Run containers
kubectl apply \
    -f app/deployment.yaml \
    -f app/service.yaml \
    -f web/deployment.yaml \
    -f web/service.yaml  \
    -f db/deployment.yaml  \
    -f db/service.yaml  \
    -f db/secret.yaml  \
    -f db/configmap.yaml \
    -f db/persistent-volume.yaml \
    -f ingress/managed-cert.yaml \
    -f ingress/managed-cert-ingress.yaml
```

## Other things you have to do for SSL configration

- Prepare your own domain(like Google Domain)
- Reserving a static external IP address [link](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address)
- DNS (DNS A record) setting to connect static external IP address with your domain.

## When you are enough to run..

```
# Make sure delete cluster not to be billed!
$ gcloud container clusters delete linebot-gke --zone asia-northeast1-a
```

## Sample Talk

<img src="https://user-images.githubusercontent.com/25422441/144426698-72fbaea0-514a-4a19-88c8-d9461f88566a.png" width="200px">
