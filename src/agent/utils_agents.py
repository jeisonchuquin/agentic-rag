from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.graphs import NetworkxEntityGraph
from langchain.chains import GraphQAChain
from ..prompts.usfq_prompts import *
from ..config import *

# INSTANCIAMOS CONOCIMIENTO DE GRAFOS
graph = NetworkxEntityGraph.from_gml("files/usfq_student_guide_large_mkd_eng.gml")

graph_chain = GraphQAChain.from_llm(
    llm, 
    graph=graph, 
    verbose=False, 
    entity_prompt=ENTITY_PROMPT
)


# AGENTE DE EVALUACIÓN DE ALUCINACIONES
hallucination_grader = HALUCCINATION_PROMPT | llm | JsonOutputParser()


# AGENTE DE EVALUACIÓN DE RELEVANCIA DE DOCUMENTOS RECUPERADOS
retrieval_grader = RETRIEVAL_PROMPT | llm | JsonOutputParser()


# AGENTE DE EVALUACIÓN DE RESPUESTA GENERADA
answe_grader = ANSWER_PROMPT | llm | JsonOutputParser()


# AGENTE DE DECISIÓN DE RUTA BASE VECTORIAL O GRAFO
question_rounter = ROUTER_PROMPT | llm | JsonOutputParser()