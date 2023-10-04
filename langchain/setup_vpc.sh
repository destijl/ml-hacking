#!/bin/bash

# $Id: $

set -e
PROJECT_ID="gcastle-gke-dev"
REGION="us-central1"
VPC_NETWORK="langchain"
PEERING_RANGE_NAME="ann-langchain-me-range"
BUCKET_URI="gs://gcastle-langchain"
DIMENSIONS=512
DISPLAY_NAME="index-langchain"
EMBEDDING_DIR="${BUCKET_URI}/banana"
DEPLOYED_INDEX_ID="langchain-endpoint"

PROJECT_NUMBER=$(gcloud projects list --filter="PROJECT_ID:'${PROJECT_ID}'" --format='value(PROJECT_NUMBER)')
VPC_NETWORK_FULL="projects/${PROJECT_NUMBER}/global/networks/${VPC_NETWORK}"

gcloud config set project ${PROJECT_ID}

# Remove the if condition to run the encapsulated code
gcloud compute networks create ${VPC_NETWORK} --bgp-routing-mode=regional --subnet-mode=auto --project=${PROJECT_ID}

# Add necessary firewall rules
gcloud compute firewall-rules create ${VPC_NETWORK}-allow-icmp --network ${VPC_NETWORK} --priority 65534 --project ${PROJECT_ID} --allow icmp
gcloud compute firewall-rules create ${VPC_NETWORK}-allow-internal --network ${VPC_NETWORK} --priority 65534 --project ${PROJECT_ID} --allow all --source-ranges 10.128.0.0/9
gcloud compute firewall-rules create ${VPC_NETWORK}-allow-ssh --network ${VPC_NETWORK} --priority 65534 --project ${PROJECT_ID} --allow tcp:22

 # Reserve IP range
gcloud compute addresses create ${PEERING_RANGE_NAME} --global --prefix-length=16 --network=${VPC_NETWORK} --purpose=VPC_PEERING --project=${PROJECT_ID} --description="peering range"

# Set up peering with service networking
# Your account must have the "Compute Network Admin" role to run the following.
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --network=${VPC_NETWORK} --ranges=${PEERING_RANGE_NAME} --project=${PROJECT_ID}
