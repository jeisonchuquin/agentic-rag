import os
import opik
from opik.integrations.langchain import OpikTracer
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PDF_PATH = 'files/manual-del-estudiante-de-grado.pdf'
LLM_MODEL = 'gpt-5-mini'
LLM_MODEL_GRAPH = 'o3'
DB_NAME = "usfq_vector_db_large"
URI = "http://localhost:19530"
PROJECT_OPIK_NAME = 'usfq_student_guide_large_o3_graph'
GRPAH_DB = "files/usfq_student_guide_large_mkd_eng.gml"
QA_DATABASE_1 = 'files/preguntasyrespuestas_clean.xlsx'
QA_DATABASE_2 = 'files/usfq-qa-dataset-v2.xlsx'
EMBEDDING_MODEL = 'text-embedding-3-large'
TOP_K = 10

opik.configure(use_local=True)
opik_tracer = OpikTracer(project_name=PROJECT_OPIK_NAME)
opik_client = opik.Opik(project_name=PROJECT_OPIK_NAME)

emmbeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

llm = ChatOpenAI(
    # temperature=0,
    model=LLM_MODEL,
    # model='gpt-4o-mini',
    openai_api_key=OPENAI_API_KEY,
    max_tokens=None,
    callbacks=[opik_tracer]
)

llm_graph = ChatOpenAI(
    # temperature=0,
    model=LLM_MODEL_GRAPH,
    # model='gpt-4o-mini',
    openai_api_key=OPENAI_API_KEY,
    max_tokens=None,
    callbacks=[opik_tracer]
)


