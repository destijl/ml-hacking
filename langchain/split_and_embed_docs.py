import json
from langchain.embeddings import VertexAIEmbeddings
from langchain.document_loaders import GCSFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import MatchingEngine

PROJECT_ID="gcastle-gke-dev"
REGION="us-central1"
BUCKET_NAME="gcastle-langchain"
BLOB="aliceinwonderland.txt"
INDEX_ID="alice"
INDEX_ENDPOINT_ID="langchaindemo"
EMBEDDING_DIR="gs://gcastle-langchain/alice-embedded"

# Define Text Embeddings model
embedding = VertexAIEmbeddings()

# Define Matching Engine as Vector Store 
#me = MatchingEngine.from_components(
#    project_id=PROJECT_ID,
#    contents_delta_uri=EMBEDDING_DIR,
#    region=REGION,
#    gcs_bucket_name=f'gs://{BUCKET_NAME}',
#    embedding=embedding,
#    index_id=INDEX_ID,
#    endpoint_id=INDEX_ENDPOINT_ID
#)

# Define Cloud Storage file loader to read a document
loader = GCSFileLoader(project_name=PROJECT_ID,
    bucket=BUCKET_NAME,
    blob=BLOB)
document = loader.load()

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
doc_splits = text_splitter.split_documents(document)

# Add embeddings of document chunks to Matching Engine
texts = [doc.page_content for doc in doc_splits]

with open("alice_embeddings.json", "w") as f:
    for textid, text in enumerate(texts):
        index = {}
        index["id"] = f"aliceinwonderland-{textid}"
        index["embedding"] = embedding.embed_query(text)
        json.dump(index, f)
        f.write("\n")
