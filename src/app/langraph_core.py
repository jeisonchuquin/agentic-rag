from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from .langraph_functions import *

memory = MemorySaver()
workflow = StateGraph(GrapState)

# Define the nodes
workflow.add_node('question_correct', question_correction_fun)
workflow.add_node('question_reviewer', question_filter_fn)
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("graphrag", graph_search)
workflow.add_node('general_response', general_response_fn) # respuesta general

# instanciamos el nodo raiz
workflow.add_edge(START, 'question_correct')


workflow.add_conditional_edges(
    'question_correct',
    route_question,
    {
        'retrieve': 'retrieve', # respuesta: nodo
        'graphrag': 'graphrag',
        'no permited': 'question_reviewer'#END
    }
)


# Add edges
workflow.add_edge('question_reviewer', 'generate')
workflow.add_edge("retrieve", "grade_documents")
workflow.add_edge("grade_documents", "generate")
workflow.add_edge("graphrag", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "general_response",
        "not useful": "general_response",
        "useful": END,
    },
)
workflow.add_edge("general_response", "generate")
app = workflow.compile(checkpointer=memory)

