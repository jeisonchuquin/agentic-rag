from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from ..prompts.usfq_prompts import *
from ..config import *

# AGENTE DE RESPUESTA TOTAL
graph_rag_chain = PROMPT | llm | StrOutputParser()


# AGENTE DE RESPUESTA RAG VECTORIAL
rag_chain = PROMPT_VEC | llm | StrOutputParser()


# AGENTE DE CORRECCIÓN DE RESPUESTA
question_correction = QUESTION_CORRECT_PROMPT | llm | StrOutputParser()


# AGENTE QUE VALIDA TEMAS SENSIBLES
question_filter = QUESTION_FILTER_PROMPT | llm | JsonOutputParser()


# AGENTE GENERAL DE RESPUESTA
general_response = GENERAL_PROMTP | llm | StrOutputParser()
