from llama_index.core import SimpleDirectoryReader,VectorStoreIndex
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

data = SimpleDirectoryReader(input_dir="./source_documents",recursive=True).load_data()

for x in data:
    c=1
    print("METADATAAAAA   " + x.metadata['file_name'])
    if (x.metadata['file_type'] == "text/plain"):
        x.metadata={"file_name": x.metadata['file_name'], "category": "API_Document"}
    elif (x.metadata['file_type'] == "application/pdf"):
        x.metadata={"file_name": x.metadata['file_name'], "category": "Official_Document"}
        
    x.excluded_embed_metadata_keys=["file_type", "file_size", "creation_date", "last_modified_date", "last_accessed_date"]
    x.excluded_llm_metadata_keys=["file_type", "file_size", "creation_date", "last_modified_date", "last_accessed_date"]
          
          
# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(data,storage_context=storage_context,show_progress=True
)