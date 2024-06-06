from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)
from dotenv import load_dotenv
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.readers.file import PDFReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.core import StorageContext
import os
#from llama_index.core.postprocessor import LLMRerank
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
#from llama_index.postprocessor.rankgpt_rerank import RankGPTRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank
#from llama_index.core.evaluation import FaithfulnessEvaluator
# from rank_gpt import permutation_pipeline

from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)

from llama_index.core import QueryBundle
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
OPENAI_API_TOKEN = os.getenv('OPENAI_API_TOKEN')

cohere_rerank = CohereRerank(api_key=COHERE_API_KEY, top_n=3)

#os.environ["OPENAI_API_KEY"] = OPENAI_API_TOKEN
model_url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q5_K_M.gguf"

llm = LlamaCPP(
     # You can pass in the URL to a GGML model to download it automatically
     model_url=model_url,
     model_path=None,
     temperature=0,
     max_new_tokens=512,
     # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
     context_window=4500,
     # kwargs to pass to __call__()
     generate_kwargs={},
     # kwargs to pass to __init__()
     # set to at least 1 to use GPU
     model_kwargs={"n_gpu_layers": 33},
     # transform inputs into Llama2 format
     messages_to_prompt=messages_to_prompt,
     completion_to_prompt=completion_to_prompt,
     verbose=True,
 )

# llm=OpenAI(
#                model="gpt-3.5-turbo-16k",
#                temperature=0,
#                api_key=OPENAI_API_TOKEN,
#    )
# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")


#evaluator = FaithfulnessEvaluator(llm=llm)

def main():
    # create collection
    chroma_collection = db.get_or_create_collection("quickstart")
    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # create your index
    index = VectorStoreIndex.from_vector_store(vector_store,storage_context=storage_context,show_progress=True)
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    
    filters = MetadataFilters(
    filters=[
        MetadataFilter(key="category", value="Official_Document"),
    ],
)
    # query_engine=index.as_query_engine(
    #     similarity_top_k=30,
    #     filters=filters,
    #     llm=llm,
    #     verbose=False)
    # return query_engine



    chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory,
    # filters=filters,
    similarity_top_k=3,
    node_postprocessors=[cohere_rerank],
    #node_postprocessors=[
         #RankGPTRerank(
            #top_n=3,
            #verbose=True,
        #)
     #],
#     new_item = permutation_pipeline(item, rank_start=0, rank_end=3, model_name='gpt-3.5-turbo', api_key='Your OPENAI Key!')
# print(new_item)

    llm=llm,
   
    verbose=False)
    
    return chat_engine

