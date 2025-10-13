from openevals.prompts import CORRECTNESS_PROMPT, RAG_HELPFULNESS_PROMPT, RAG_GROUNDEDNESS_PROMPT, RAG_RETRIEVAL_RELEVANCE_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from opik.evaluation.metrics import base_metric, score_result
from typing import Any
from ..config import OPENAI_API_KEY


class LLMJudgeMetric(base_metric.BaseMetric):
    def __init__(self, name: str = "Factuality check", model_name: str = "gpt-4o"):
        self.name = name
        self.model_name = model_name
        self.llm_client = ChatOpenAI(            
            model=self.model_name,
            openai_api_key=OPENAI_API_KEY,
            max_tokens=None,            
        )
        
        
        match name:
            case 'Correctness':
                PROMPT = CORRECTNESS_PROMPT
            
            case 'Helpfulness':
                PROMPT = RAG_HELPFULNESS_PROMPT
            
            case 'Groundedness':
                PROMPT = RAG_GROUNDEDNESS_PROMPT
            
            case 'Retrieval_relevance':
                PROMPT = RAG_RETRIEVAL_RELEVANCE_PROMPT
            
            case _:
                raise Exception('Nombre de metrica no definida')
        
        JSON_PROMPT = '''
Remember that all is about Universidad San Francisco de Quito (USFQ).

It is crucial that you provide your answer in the following JSON format:

{{

    "score": <your score between 0.0 and 1.0>,

    "reason": ["reason 1", "reason 2"]

}}

Reasons amount is not restricted. Output must be JSON format only.
        '''
        PROMPT = PROMPT + JSON_PROMPT
        self.llm_judge = PromptTemplate.from_template(PROMPT) | self.llm_client | JsonOutputParser()
    
    def score(self, inputs: str, outputs: str, context: str, reference_outputs: str, **ignored_kwargs: Any):
        """
        Score the output of an LLM.

        Args:
            output: The output of an LLM to score.
            **ignored_kwargs: Any additional keyword arguments. This is important so that the metric can be used in the `evaluate` function.
        """        
        # Generate and parse the response from the LLM       
        response = self.llm_judge.invoke(
            {
                "inputs": inputs,
                "outputs": outputs,
                'context': context,
                "reference_outputs": reference_outputs
            }, 
            # config={'callbacks': [opik_tracer]}
        )

        response_score = float(response['score'])
        reasons = response['reason']
        reasons = '\n'.join(reasons)

        # return response
        return score_result.ScoreResult(
            name=self.name,
            value=response_score,            
            reason=reasons
        )



