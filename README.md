# blockchainETL-airflow-eks-cluster
Building an airflow on Amazon Elastic Kubernetes Service
## What is this about?
Code in this repository along with this Introduction is able to:
1. define and deploy a customized k8s cluster on AWS EKS(Elastic Kubernetes Service)
2. run airflow dags auto-synchronized with a customized github repository URL (in this case, this address point to https://github.com/GGtray/airflow-dags.git)
## How to use it? (on MacOS)
### Before using it, you will need
- An AWS account (with enough money in it, eks costs, add IAM role premisson via configuring policy)
- AWS CLI
- kubectl
- wget
### Spining up K8s and connect it to your local computer (waiting for optimizing with terragrunt)
- Step 1: Configure awscli for Authentication
```
$ aws configure
AWS Access Key ID [None]: YOUR_AWS_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_AWS_SECRET_ACCESS_KEY
Default region name [None]: YOUR_AWS_REGION
Default output format [None]: json
```
this step makes you login your aws account on your computer, thus charge you after your cluster spinned up.
- Step 2: Provision the EKS cluster
```
$ terraform init
$ terraform apply
```
wait with patience, it is pretty normal to run for 30min.
- Step 3: Configure kubectl
```
$ aws eks --region us-east-2 update-kubeconfig --name [name in the output]
$ terraform apply
```
this step will asure your kubectl is connected to the cluster, run
```
$ kubectl cluster-info
```
to check this connection out!
### (Option) check cluster through DashBoard

### Run airflow
- Step 1: configure vales.yml
```
$ cd charts/stable/airflow
```
change as such: 
```
## configs for the DAG git repository & sync container
  ##
  git:
    ## url of the git repository
    ##
    ## EXAMPLE: (HTTP)
    ##   url: "https://github.com/torvalds/linux.git"
    ##
    ## EXAMPLE: (SSH)
    ##   url: "ssh://git@github.com:torvalds/linux.git"
    ##
    url: "https://github.com/GGtray/airflow-dags.git"

    ## the branch/tag/sha1 which we clone
    ##
    ref: master

   ...
    gitSync:
      ## enable the git-sync sidecar container
      ##
      enabled: true

      ## resource requests/limits for the git-sync container
      ##
      ## NOTE:
      ## - when `workers.autoscaling` is true, YOU MUST SPECIFY a resource request
      ##
      ## EXAMPLE:
      ##   resources:
      ##     requests:
      ##       cpu: "50m"
      ##       memory: "64Mi"
      ##
      resources: {}
```
- Step 2: start up airflow and check on the airflow Web UI
```
helm install stable/airflow -f values.yaml --generate-name
export POD_NAME=$(kubectl get pods --namespace default -l "component=web,app=airflow" -o jsonpath="      {.items[0].metadata.name}")
echo http://127.0.0.1:8080
kubectl port-forward --namespace default $POD_NAME 8080:8080
```
visit: http://localhost:8080 for airflow dashborad

- Optional: 
if you need to update this values.yaml file, use below
```
kubectl get service
# find your airflow release id here
helm upgrade <airflow release id> -f values.yaml stable/airflow
```
if you wanna see if the git-sync is working currently
```
kubectl get pods
# find your pod id running airflow-*-web here
kubectl logs <airflow-*-web id> git-sync
```

## How to configure it?
### Configure Kubernetes (via conigure .tf files below)
.tf files | function
------------ | -------------
vpc.tf | provisions a VPC, subnets and availability zones using the AWS VPC Module. 
security-groups.tf | provisions the security groups used by the EKS cluster.
eks-cluster.tf | provisions all the resources (AutoScaling Groups, etc...) 
### Configure Airflow Dags

fields in values.yaml | function
------------ | -------------
dags/ git / url | git repository
dags/ gitSync/enable | true
dags/gitSync/refreshTime | 10/60 s


