from langchain_core.prompts import PromptTemplate

# PROMT DE RESPUESTA USANDO INFORMACIÓN VECTORIAL
PROMPT_VEC = PromptTemplate.from_template(
'''
Eres un asistente de preguntas y respuestas especializado en el manual del estudiante de la USFQ.
Usa el contexto proporcionado recuperado de una base vecotorial.
Si no hay evidencia suficiente, responde con incertidumbre.
Cita explícitamente los fragmentos relevantes (archivo y sección) cuando sea posible.
La información del contexto está abajo.

INICIO CONTEXTO
Vector context: {context}
FIN DE CONTEXTO

Dado la información del contexto y sin conocimiento previo, responde la pregunta.

Pregunta: {question}

Respuesta:
'''    
)


# PROMPT PARA OBTENER NOMBRES DE ENTIDADES PARA RECUPERACIÓN DE GRAFOS
ENTITY_PROMPT = PromptTemplate.from_template(''' 
Extrae todas las entidades del siguiente texto. Como pauta general, los nombres propios suelen escribirse con mayúscula inicial. Debe extraer todos los nombres y lugares sin excepción.

Devuelve el resultado como una lista separada por comas y con las siguientes formas de escritura: todas mayúsculas, todas minúsculas y la letra inicial con mayúscula, o NONE si no hay nada relevante que devolver.

EJEMPLO
Estoy intentando mejorar las interfaces de Langchain, la experiencia de usuario, sus integraciones con diversos productos que el usuario podría desear... muchas cosas.
Resultado: LANGCHAIN, langchain, Langchain
FIN DEL EJEMPLO

EJEMPLO
Estoy tratando de mejorar las interfaces de Langchain, la experiencia de usuario, sus integraciones con varios productos que el usuario podría desear... muchas cosas. Estoy trabajando con Sam.
Resultado: LANGCHAIN, langchain, Langchain, SAM, Sam, sam
FIN DEL EJEMPLO

{input}

Output:
''')


# PROMPT GENERA DE RESPUESTA QUE USA INFORMACIÓN RECUPERADA DE VECTOR Y GRAFO
PROMPT = PromptTemplate.from_template(
'''
Eres un asistente de preguntas y respuestas especializado en el manual del estudiante de la USFQ.
Usa el contexto proporcionado recuperado de una base vecotorial y de un grafo de conocimiento. 
Si no hay evidencia suficiente, responde con incertidumbre.
Cita explícitamente los fragmentos relevantes (archivo y sección) cuando sea posible.
La información del contexto está abajo.

---------------------
Vector context: 
{context}
---------------------
Graph context: 
{graph_context}
---------------------


Dado la información del contexto y sin conocimiento previo, responde la pregunta.

Pregunta: {question}

Respuesta:
'''    
)


# PROMT PARA METRICA DE ALUCINACIóN
HALUCCINATION_PROMPT = PromptTemplate.from_template('''
Eres un evaluador que determina si una respuesta se basa en o está respaldada por un conjunto de hechos.
Asigna una puntuación binaria "yes" o "no" para indicar si la respuesta se basa en o está respaldada por un conjunto de hechos. 
Proporcione la puntuación binaria como un JSON con una única clave "score" y sin preámbulos ni explicaciones.

Estos son los hechos:
{documents}

Esta es la respuesta:
{generation}    
'''
)


# PROMT PARA VERIFICAR VALIDEZ DE UNA RECUPERACIÓN VECOTRIAL
RETRIEVAL_PROMPT = PromptTemplate.from_template('''
Eres un evaluador que valora la relevancia de un documento recuperado para la pregunta de un usuario. 
Si el documento contiene palabras clave relacionadas con la pregunta del usuario, clasifícalo como relevante. 
No es necesario que sea una prueba rigurosa. 
El objetivo es filtrar las recuperaciones erróneas.

Asigna una puntuación binaria "yes" o "no" para indicar si el documento es relevante para la pregunta.
Proporcione la puntuación binaria como un JSON con una única clave "score" y sin preámbulo ni explicación.

Este es el documento recuperado:
{document}

Esta es la pregunta del usuario:
{question}
'''
)


# PROMT PARA VERIFICAR SI LA RESPUESTA RESPONDE A LA PREGUNTA
ANSWER_PROMPT = PromptTemplate.from_template('''
Eres un evaluador que determina si una respuesta es útil para resolver una pregunta. 
Asigna una puntuación binaria "yes" o "no" para indicar si la respuesta es útil para resolver una pregunta.
Proporciona la puntuación binaria como un JSON con una sola clave "score" y sin preámbulos ni explicaciones.

Esta es la respuesta:
{generation}

Esta es la pregunta: {question}
'''                                             
)


# PROMPT PARA DECIDIR QUÉ TIPO DE RECUPERACIÓN REALIZARÁ
ROUTER_PROMPT = PromptTemplate.from_template('''
Eres un experto en direccionar una pregunta del usuario para que sea respondida con la apropiada fuente de datos.
Tienes 2 opciones:

1. 'vectorstore': Úsalo pora responder preguntas de carácter general de la USFQ.
2. 'graphrag': Úsalo para responder preguntas de puntuales de carácter qué, cómo, cúando, dónde, etc.

No es necesario ser estricto con las palabras clave de la pregunta relacionada con estos temas.
Elije la opción más adecuada en función de la naturaleza de la pregunta.

Retorna un JSON con una sola clave 'datasource' sin preámbulos ni explicaciones. Los valores deben ser uno de estos: 'vectorstore' o 'graphrag'

Esta es la pregunta a direccionar:
{question}
'''
)


# PROMPT PARA CORREGIR LA PREGUNTA INGRESADA
QUESTION_CORRECT_PROMPT = PromptTemplate.from_template('''
Eres un experto en revisar la ortografía de la pregunta del usuario independientemente del idioma en el que se haga la pregunta.

Tu trabajo es verificar que la pregunta esté bien escrita y formulada, si no la está, tienes que corregir las faltas de ortografía,
si es necesario puedes reformular la pregunta para que tenga sentido, únicamente devuelve la pregunta corregida o reformulada, no expliques los cambios.

Esta es la pregunta:
{question}
'''
)


# PROMPT PARA TRATAR TEMAS SENSIBLES EN LA PREGUNTA
QUESTION_FILTER_PROMPT = PromptTemplate.from_template('''
Eres un experto en verificar que la pregunta del usuario esté relacionado con temas relacionados al manual del estudiante de la Universidad San Francisco de Quito (USFQ).

Si la pregunta tiene que ver con temas del manual del estudiante de la USFQ, dime "yes", si la pregunta contiene temas sensibles
como ideología de género, política, partidos políticos, discriminación, xenofobia, racismo, guerras, esclavitud y otros temas
sensibles que consideres responde de forma cordial que no puedes responder porque la pregunta no tiene que ver con la USFQ.

Verifica que la pregunta esté relacionada con el context proporcionado, si lo está, responde "yes". 

Proporciona la respuesta en formato JSON, con una única clave "resp".


Esta es la pregunta: {question}

Este es el contexto: {context}
'''    
)



# PROMTP GENÉRICO
GENERAL_PROMTP = PromptTemplate.from_template(
'''
Eres un asistente que ayuda a solventar dudas sobre cosas generales de la Universidad San Francisco de Quito a 
estudiantes de la universidad, por lo que debes responder de manera cordial, responde con todos los detalles que 
puedas.


Pregunta: {question}

Respuesta:
'''
)
