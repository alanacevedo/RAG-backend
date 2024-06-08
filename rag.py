from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbedding
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings, load_index_from_storage
from huggingface_hub import login
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from dotenv import load_dotenv
import os 

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
PERSIST_DIR = os.getenv("PERSIST_DIR")
login(token=HF_TOKEN)

llm = HuggingFaceInferenceAPI(
    model_name="HuggingFaceH4/zephyr-7b-beta",
    api_key=HF_TOKEN 
)

embed_model = HuggingFaceInferenceAPIEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    api_key=HF_TOKEN)

Settings.llm = llm
Settings.embed_model = embed_model

if not os.path.exists(PERSIST_DIR):
    # load files
    documents = SimpleDirectoryReader("data").load_data()

    # parse document into nodes
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)    
    
    # storage context => vector files/database
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    #load index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context=storage_context)
    

user_prompt = "What is a flow map?"

query_engine = index.as_query_engine()
response = query_engine.query(user_prompt)
print(response)