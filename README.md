# blockchainETL-airflow-eks-cluster
Building an airflow on Amazon Elastic Kubernetes Service
## What is this about?

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
- Step 2: Provision the EKS cluster
```
$ terraform init
$ terraform apply
```
- Step 3: Configure kubectl
```
$ aws eks --region us-east-2 update-kubeconfig --name [name in the output]
$ terraform apply
```
### Run airflow
- Step 1: Create and switch name space
```
$ kubectl create namespace airflow
$ kubectl config set-context dev1 --namespace=airflow
```
- Step 2: Configure helm chart for Postgres 
```
$ git clone https://github.com/helm/charts.git
$ cd charts/stable/airflow
```
configure vales.yml
```
## PostgreSQL port
service:
    port: 5432
  ## PostgreSQL User to create.
  postgresUser: postgres
  ##
  ## PostgreSQL Password for the new user.
  ## If not set, a random 10 characters password will be used.
  postgresPassword: airflow
  ##
  ## PostgreSQL Database to create.
  postgresDatabase: airflow
```
- Step 3: configure airflow dag via dockerhub pull
```
  image:
    ##
    ## docker-airflow image
    repository: [the docker hub repo path]
    ##
    ## image tag
```
- Step 4: start up airflow and check
```
$ helm install stable/airflow -f values.yaml
$ kubectl get service
$ kubectl port-forward service/[your airflow web service name] 8080:8080
```
visit: http://localhost:8080 for airflow dashborad

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
image / url | docker hub repo path



