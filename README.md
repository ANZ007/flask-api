# Flask API
Bangkit Capstone Project

# Deployment on GCP
All commands must be run in cloudshell

## Using Compute Engine with Docker

### Set a Project in Cloudshell
```
gcloud config set project [YOUR PROJECT ID]
```

### Create a Instance in Compute Engine
```
gcloud beta compute instances create capstone-server --zone=asia-southeast1-a --machine-type=n1-standard-1 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --tags=http-server --image=ubuntu-2004-focal-v20210510 --image-project=ubuntu-os-cloud --boot-disk-size=30GB --boot-disk-type=pd-balanced --boot-disk-device-name=capstone-server --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --reservation-affinity=any
```

### SSH into Created Instance
```
gcloud beta compute ssh --zone "asia-southeast1-a" "capstone-server"
```

### Update Repo and Upgrade the System
```
sudo apt update && sudo apt upgrade
```

### Install packages to allow apt to use a repository over HTTPS
``` 
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release 
```

### Add Docker GPG key
``` 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 
```

### Install Docker
```
sudo apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Run the Container using Docker Image
```
docker run -p 80:8000 -d --restart=unless-stopped anz007/flask-api
```


## Using Cloud Run

### Pull Image from Docker Hub 
```
docker pull anz007/flask-api
```

### Tag the Image
```
docker tag anz007/flask-api gcr.io/${GOOGLE_CLOUD_PROJECT}/flask-api
```

### Push the Image to Container Registry GCP
```
docker push gcr.io/${GOOGLE_CLOUD_PROJECT}/flask-api
```

### Deploy on Cloud Run
```
gcloud run deploy capstone-server --image=gcr.io/${GOOGLE_CLOUD_PROJECT}/flask-api \
--allow-unauthenticated --port=8000 --memory=4096Mi --platform=managed \
--region=asia-southeast1
```

## Using App Engine (Not Tested)

### Clone the Repository
```
git clone http://github.com/ANZ007/flask-api
```
### Move dir to Repository
```
cd flask-api
```

### Deploy on App Engine
```
gcloud app create
gcloud app deploy
```
in ``` gcloud app create``` select the closest region and if there is confirmation type y