
### Steps to Run Locally

### Clone Code 

```
$ git clone https://github.com/meabhishekkumar/deep-learning-production.git
cd deep-learning-production

```


### Set Project ID, Zone and Deployment

```
PROJECT_ID=nissan-helios-189503
gcloud config set project $PROJECT_ID
ZONE=us-central1-a
DEPLOYMENT_NAME=ak-test-deployment
```

setup Kubernetes with Kubeflow

use [Deploy Kubeflow](https://deploy.kubeflow.cloud/#/deploy) to setup K8S cluster with Kubeflow

nissan-helios-189503
ak-test-deployment

### Navigate to book-recommendation

```
cd books-recommendation
WORKING_DIR=$(pwd)
```

### Connect with the Cluster

```
gcloud container clusters get-credentials \
    $DEPLOYMENT_NAME --zone $ZONE --project $PROJECT_ID
```

Set context

```
kubectl config set-context $(kubectl config current-context) --namespace=kubeflow
kubectl get all
```


### Install KSONNET

```
// download ksonnet for linux (including Cloud Shell)
// for macOS, use ks_0.13.0_darwin_amd64 for Linux use : ks_0.13.0_linux_amd64
KS_VER=ks_0.13.0_darwin_amd64

//download tar of ksonnet
wget --no-check-certificate \
    https://github.com/ksonnet/ksonnet/releases/download/v0.13.0/$KS_VER.tar.gz

//unpack file
tar -xvf $KS_VER.tar.gz

//add ks command to path
PATH=$PATH:$(pwd)/$KS_VER
```

### Create Ksonnet Project 

```
KS_NAME=my_ksonnet_app
ks init $KS_NAME
cd $KS_NAME
```

list environment and component 

```
ks env list
ks component list
```
Copy components 

```
cp $WORKING_DIR/ks_app/components/* $WORKING_DIR/$KS_NAME/components
ks component list
```

add kubeflow to resources 
```
VERSION=v0.4.1
ks registry add kubeflow \
    github.com/kubeflow/kubeflow/tree/${VERSION}/kubeflow
ks pkg install kubeflow/tf-serving@${VERSION}
```

### Training 

Set Bucket Name 

```
BUCKET_NAME=ak-$KS_NAME-$PROJECT_ID
gsutil mb gs://$BUCKET_NAME/
```
Build Training Image 


```
//set the path on GCR you want to push the image to
TRAIN_PATH=us.gcr.io/$PROJECT_ID/ak-kubeflow-train

//build the tensorflow model into a container
//container is tagged with its eventual path on GCR, but it stays local for now
docker build $WORKING_DIR/train -t $TRAIN_PATH -f $WORKING_DIR/train/Dockerfile.model
```
Check locally

```
docker run -it $TRAIN_PATH
```

Push Docker image

```
//allow docker to access our GCR registry
gcloud auth configure-docker --quiet

//push container to GCR
docker push $TRAIN_PATH
```


docker image rm $TRAIN_PATH



Train on the cluster

```


//set the parameters for this job
ks param set train image $TRAIN_PATH
ks param set train name "train-book-recsys-1"
ks param set train trainSteps 200
ks param set train modelDir gs://${BUCKET_NAME}/model
ks param set train exportDir gs://${BUCKET_NAME}/export

```

check service account access 
```
gcloud --project=$PROJECT_ID iam service-accounts list | grep $DEPLOYMENT_NAME
```

check kubernetes secrets

```
kubectl describe secret user-gcp-sa
```

Set Google Application Credentials 

```
ks param set train secret user-gcp-sa=/var/secrets
ks param set train envVariables \
    GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/user-gcp-sa.json
```

Run the training job

```
ks apply default -c train
```

Describe Job

```
kubectl describe tfjob
```

Check logs 
```
kubectl logs -f train-book-recsys-1-chief-0
```
### Monitoring

```
LOGDIR=gs://${BUCKET_NAME}/model
ks param set tensorboard logDir ${LOGDIR}

ks param set tensorboard secret user-gcp-sa=/var/secrets
ks param set tensorboard envVariables \
    GOOGLE_APPLICATION_CREDENTIALS=/var/secrets/user-gcp-sa.json

ks apply default -c tensorboard
kubectl port-forward service/tensorboard-tb 8092:80

```

### Serving

Set parameters and deploy serving

```
ks param set book-recsys-deploy-gcp modelBasePath gs://${BUCKET_NAME}/export
ks param set book-recsys-deploy-gcp modelName book-recsys
ks apply default -c book-recsys-deploy-gcp
```

check log
```
kubectl logs -l app=book-recsys
```

deploy service

```
ks apply default -c book-recsys-service
```

```
kubectl describe service book-recsys-service
```

### Deploy UI

build UI Image 

```
// set the path on GCR you want to push the image to
UI_PATH=us.gcr.io/$PROJECT_ID/ak-kubeflow-web-ui

// build the web-ui directory
docker build $WORKING_DIR/web-ui -t $UI_PATH

// allow docker to access our GCR registry
gcloud auth configure-docker --quiet

// push the container to GCR
docker push $UI_PATH
```

//delete docker image
```
docker image rm $UI_PATH
```

set parameters and deploy

```
// set parameters
ks param set web-ui image $UI_PATH
ks param set web-ui type LoadBalancer

// apply to cluster
ks apply default -c web-ui
```

kubectl get service web-ui


### Katib 
kubectl apply -f $WORKING_DIR/katib/hyper-parameter_random.yaml
kubectl get studyjob
kubectl describe studyjobs books-recsys-example


### Clean up 