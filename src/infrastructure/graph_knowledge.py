import tiktoken
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_text_splitters import MarkdownHeaderTextSplitter
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.prompts import PromptTemplate
from langchain_community.graphs import NetworkxEntityGraph
from ..config import PDF_PATH, llm_graph



tokenizer = OpenAITokenizer(    
    tokenizer=tiktoken.get_encoding("cl100k_base"), # text-embedding-3-large
    max_tokens=8192  # context window length required for OpenAI tokenizers, si el chunk es demasiado largo, lo cortará a esta longitud
)

chunker = HybridChunker(
    tokenizer=tokenizer,
    max_tokens=8192,
    merge_peers=True,  # merge chunks that are too close to each other
)

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

# Construcción en inglés
graph_transformer = LLMGraphTransformer(
    llm=llm_graph,
    prompt=PromptTemplate.from_template(
'''
You are a top-tier algorithm designed for extracting information in
structured formats to build a knowledge graph. Your task is to identify
the entities and relations requested with the user prompt from a given
text. You must generate the output in a JSON format containing a list
with JSON objects. Each object should have the keys: head,
head_type, relation, tail, and tail_type.
Your task is to extract relationships from text strictly adhering
to the provided schema. The relationships can only appear
between specific node types are presented in the schema format
like: (Entity1Type, RELATIONSHIP_TYPE, Entity2Type) /n
Attempt to extract as many entities and relations as you can. Maintain
Entity Consistency: When extracting entities, it's vital to ensure
consistency. If an entity, such as John Doe, is mentioned multiple
times in the text but is referred to by different names or pronouns
(e.g., Joe, he), always use the most complete identifier for
that entity. The knowledge graph should be coherent and easily
understandable, so maintaining consistency in entity references is
crucial.,
IMPORTANT NOTES:\n- Don't add any explanation and text. ,
'''
    )    
)

graph_documents = graph_transformer.convert_to_graph_documents(splits)

# instanciamos el grafo
graph = NetworkxEntityGraph()

# creamos nodos
for doc in graph_documents:
    for node in doc.nodes:
        graph.add_node(node.id)

# añadimos arcos
for doc in graph_documents:
    for edge in doc.relationships:
        graph._graph.add_edge(edge.source.id, edge.target.id, relation=edge.type)

graph.write_to_gml("../files/usfq_student_guide_large_mkd_eng.gml")
