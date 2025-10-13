from typing_extensions import TypedDict
from typing import List
from ..agent.response_agents import *
from ..agent.utils_agents import *
from ..infrastructure.retrievers import *
from ..config import format_docs

class GrapState(TypedDict):
    '''
    Representa el estado del grafo
    
    Attributes:
        question: question
        generation: LLM generation
        not_permited: whether to generate not_permited answer
        documents: list of documents
        graph_context: results from graph search
    '''
    
    question: str
    generation: str
    not_permited: str
    documents: List[str]
    graph_context: str


def question_correction_fun(state):
    '''
    Corrige la pregunta del usuario
    
    Args:
        state (dict): The current graph state

    Returns:
        state (dict): The question corrected
    '''

    # print("---QUESTION CORRECTION--")
    question = state['question']
    
    question = question_correction.invoke(
        {
            'question': question
        }
    )
    
    return {'question': question}


def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    # print("---RETRIEVE---")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}



def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    # print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []    
    for d in documents:
        score = retrieval_grader.invoke(
            {
                "question": question, 
                "document": d.page_content
            }
        )
        grade = score["score"]
        
        # Document relevant
        if grade.lower() == "yes":
            # print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        
        continue
        
        # Document not relevant
        # else:
        #     # print("---GRADE: DOCUMENT NOT RELEVANT---")
        #     # We do not include the document in filtered_docs
        #     # We set a flag to indicate that we want to run web search
        #     web_search = "Yes"
        #     continue
    return {
        "documents": filtered_docs, 
        "question": question,         
    }



def graph_search(state):
    """
    Perform GraphRAG search using Neo4j

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updated state with graph search results
    """
    # print("---GRAPH SEARCH---")
    question = state["question"]

    # Use the graph_rag_chain to perform the search
    result = graph_chain.invoke({"query": question})

    # Extract the relevant information from the result
    # Adjust this based on what graph_rag_chain returns
    graph_context = result.get("result", "")

    # You might want to combine this with existing documents or keep it separate
    return {
        "graph_context": graph_context, 
        "question": question
    }


def question_filter_fn(state): #! nodo
    '''
    
    '''

    question = state['question']
    documents = state.get('documents', [])
    
    score_filter = question_filter.invoke({'question': question, 'context': format_docs(documents)})
    
    return {
        'question': question,
        'not_permited': score_filter['resp']
    }


def generate(state):
    """
    Generate answer using RAG on retrieved documents and graph context

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    # print("---GENERATE---")
    question = state["question"]
    documents = state.get("documents", [])
    graph_context = state.get("graph_context", "")
    not_permited = state.get('not_permited', "")

    if not_permited == "":
        # Composite RAG generation    
        generation = graph_rag_chain.invoke(
            {
                "question": question, 
                "context": format_docs(documents), 
                "graph_context": graph_context#['result']
            }
        )
    
    else:
        generation = not_permited    
    
    return {
        "documents": documents,
        "question": question,
        "generation": generation,
        "graph_context": graph_context,
    }



### Conditional edge
def route_question(state):
    
    # print("---ROUTE QUESTION---")
    question = state["question"]
    documents = state.get('documents', [])
    # print(question)
    
    score_filter = question_filter.invoke({'question': question, 'context': format_docs(documents)})
    
    if score_filter['resp'] == 'yes':
        pass
    else:        
        return 'no permited'
    
    
    
    source = question_rounter.invoke({"question": question})
    # print(source)
    # print(source["datasource"])

    if source["datasource"] == "graphrag":
        # print("---TRYING GRAPH SEARCH---")
        graph_result = graph_search({"question": question})
        if graph_result["graph_context"] != "No lo sé.":
            return "graphrag"
        else:
            # print("---NO RESULTS IN GRAPH, FALLING BACK TO VECTORSTORE---")
            return "retrieve"
    elif source["datasource"] == "vectorstore":
        # print("---ROUTE QUESTION TO VECTORSTORE RAG---")
        return "retrieve"
    # elif source["datasource"] == "web_search":
    #     # print("---ROUTE QUESTION TO WEB SEARCH---")
    #     return "websearch"



### Conditional edge
def grade_generation_v_documents_and_question(state):
    """
    Determines whether the generation is grounded in the document and answers question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Decision for next node to call
    """

    # print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state.get("documents", "")
    generation = state["generation"]
    not_permited = state.get('not_permited', "")
    graph_context = state.get('graph_context', "")
    
    
    if isinstance(documents, list):
        documents = format_docs(documents)
        documents = documents + "\n" + graph_context
    elif isinstance(documents, str):
        documents = documents + "\n" + graph_context
    

    if documents:
        score = hallucination_grader.invoke(
            {
                "documents": documents, 
                "generation": generation
            }
        )
        grade = score.get("score", "").lower()
    else:
        grade = 'yes'
    
    
    if not_permited != "":
        return 'useful'

    # Check hallucination
    if grade == "yes":
        # print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        
        # Check question-answering
        # print("---GRADE GENERATION vs QUESTION---")
        score = answe_grader.invoke(
            {
                "question": question, 
                "generation": generation
            }
        )
        grade = score["score"]
        
        if grade == "yes":
            # print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            # print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        # print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"



def general_response_fn(state):
    
    
    # print("---GENERAL RESPONSE---")
    question = state["question"]
    
    general_context = general_response.invoke({'question': question})
    
    return {'graph_context': general_context}

