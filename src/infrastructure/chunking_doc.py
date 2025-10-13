import tiktoken
from pymilvus import Collection, MilvusException, connections, db, utility
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_milvus.vectorstores import Milvus
from docling.chunking import HybridChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from ..config import emmbeddings, URI, PDF_PATH

# creamos nuestra base vectorial
tokenizer = OpenAITokenizer(    
    tokenizer=tiktoken.get_encoding("cl100k_base"), # text-embedding-3-large
    max_tokens=8192  # context window length required for OpenAI tokenizers, si el chunk es demasiado largo, lo cortará a esta longitud
)

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=8192,
    merge_peers=True,  # merge chunks that are too close to each other
)

conn = connections.connect(host="127.0.0.1", port=19530)



db_name = "usfq_vector_db_large"
try:
    existing_databases = db.list_database()
    
    if db_name in existing_databases:

        print(f"Database '{db_name}' already exists.")        
        db.using_database(db_name)

        # eliminamos todas las colecciones en la base
        collections = utility.list_collections()
    
        for collection_name in collections:
            collection = Collection(name=collection_name)
            collection.drop()
            print(f"Collection '{collection_name}' has been dropped.")

        db.drop_database(db_name)
        print(f"Database '{db_name}' has been deleted.")

    else:
    
        print(f"Database '{db_name}' does not exist.")
        database = db.create_database(db_name)
        print(f"Database '{db_name}' created successfully.")

except MilvusException as e:
    print(f"An error occurred: {e}")



# Obtenemos los chunks en formato Document, para que sea compatible con Milvus de langchain
EXPORT_TYPE = ExportType.MARKDOWN

loader = DoclingLoader(
    file_path=PDF_PATH,
    export_type=EXPORT_TYPE,
    chunker=chunker,
)
docs = loader.load()


if EXPORT_TYPE == ExportType.DOC_CHUNKS:
    splits = docs

elif EXPORT_TYPE == ExportType.MARKDOWN:
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header_1"),
            ("##", "Header_2"),
            ("###", "Header_3"),
        ],
    )
    splits = [split for doc in docs for split in splitter.split_text(doc.page_content) if len(split.page_content) < 65535] # 65535 es la longitud máxima de milvus para un campo de tipo string

else:
    raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")


# GUARDAMOS LOS CHUNCKS EN BASE
vector_store_saved = Milvus.from_documents(
    documents=splits, # necesito que los chunks sean tipo Document
    embedding=emmbeddings,
    collection_name="usfq_student_guide_large_mkd",
    connection_args={"uri": URI, "token": "root:Milvus", "db_name": db_name},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    consistency_level="Strong",
    drop_old=False,
)
