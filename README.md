# Line TODO Management Bot

## Overview

- Add your todo task.
- Delete your completed task if you type the task's name.
- Delete all your task if you type "クリア" or "clear"

### Techs

- Python 3.8.1
- Flask
- xserver (Hosting server)
- mysql

### How to run with docker-compose

```
$ pwd
/path/your/dir/linebot/
# Build & Run containers
$ docker-compose up
# Stop & Delete containers
$ docker-compose down --rmi all --volumes --remove-orphans
```

### How to run on GKE

```
$ pwd
/path/your/dir/linebot/
# Build & Run containers
$ kubectl apply -f app/deployment.yaml -f app/service.yaml -f web/deployment.yaml -f web/service.yaml
# Delete service, deployment
$ kubectl service deployment app-server linebot-nginx
$ kubectl delete deployment app-server linebot-nginx
```

### Sample Talk

<img src="https://user-images.githubusercontent.com/25422441/144426698-72fbaea0-514a-4a19-88c8-d9461f88566a.png" width="200px">
