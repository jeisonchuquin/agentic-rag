from langchain_community.graphs import NetworkxEntityGraph
from langchain_milvus.vectorstores import Milvus
from ..config import *


vector_store_saved = Milvus(
    embedding_function=emmbeddings,
    connection_args={"uri": URI, "token": "root:Milvus", "db_name": DB_NAME},
    collection_name="usfq_student_guide_large_mkd",
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    consistency_level="Strong", 
)

retriever = vector_store_saved.as_retriever(search_kwargs={"k": TOP_K})


graph = NetworkxEntityGraph.from_gml(GRPAH_DB)