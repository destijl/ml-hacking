import os
import json

from google.cloud import aiplatform

DISPLAY_NAME="index-langchain"
EMBEDDING_DIR="gcastle-langchain"
BUCKET_URI="gs://gcastle-langchain"
EMBEDDING_DIR=f"{BUCKET_URI}/alice-embedded"
VPC_NETWORK_FULL="projects/305419152720/global/networks/langchain"

my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name=DISPLAY_NAME,
    contents_delta_uri=EMBEDDING_DIR,
    dimensions=512,
    approximate_neighbors_count=150,
    distance_measure_type="DOT_PRODUCT_DISTANCE",
)

my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name=f"{DISPLAY_NAME}-endpoint",
    network=VPC_NETWORK_FULL)
