
`http://127.0.0.1:9091/webui/`



Fuentes que se utilizaron para construir un RAG:

Milvus:
[text](https://python.langchain.com/docs/integrations/vectorstores/milvus/)
    https://www.youtube.com/watch?v=OD5FS7qUfBQ
    https://milvus.io/api-reference/pymilvus/v2.4.x/MilvusClient/Collections/create_schema.md
    https://milvus.io/docs/es/quickstart.md

Docling:
    [text](https://www.youtube.com/watch?v=9lBTS5dM27c)
    [text](https://www.youtube.com/watch?v=zSCxbqgqeJ8)
    [text](https://docling-project.github.io/docling/examples/hybrid_chunking/#configuring-tokenization)

RAG:
    [text](https://docling-project.github.io/docling/examples/rag_langchain/#ingestion)
    [text](https://python.langchain.com/docs/integrations/document_loaders/docling/)


Por hacer:
    [text](https://python.langchain.com/docs/tutorials/rag/)

Guias:
    [text](https://www.apideck.com/blog/building-a-local-rag-chat-app-with-reflex-langchain-huggingface-and-ollama)
    [text](https://github.com/TAMustafa/Local_Chat_RAG/tree/main)

Langchain:
    [text](https://docs.smith.langchain.com/observability/tutorials/observability)

Embeddings:
    [text](https://platform.openai.com/docs/guides/embeddings)


https://www.nb-data.com/p/rag-evaluation-monitoring-and-logging
https://www.comet.com/docs/opik/cookbook/ragas
https://github.com/comet-ml/opik
https://www.comet.com/docs/opik/evaluation/metrics/overview
https://www.comet.com/docs/opik/evaluation/metrics/context_precision
https://www.comet.com/docs/opik/evaluation/metrics/custom_model
https://www.comet.com/docs/opik/cookbook/langchain
https://www.comet.com/docs/opik/evaluation/evaluate_agents
https://github.com/langchain-ai/langchain/discussions/26109
https://github.com/langchain-ai/langchain/discussions/18309

https://medium.com/@fatimaparada.taboada/rag-on-csv-data-with-knowledge-graph-using-rdflib-rdflib-neo4j-and-langchain-4b12a114a20e
https://python.langchain.com/docs/integrations/graphs/
https://python.langchain.com/docs/integrations/graphs/rdflib_sparql/
https://mlabonne.github.io/blog/posts/Article_Improve_ChatGPT_with_Knowledge_Graphs.html
https://python.langchain.com/docs/how_to/graph_constructing/
https://neo4j.com/blog/developer/graphrag-agent-neo4j-milvus/
https://medium.com/data-science-in-your-pocket/graphrag-using-langchain-31b1ef8328b9
https://python.langchain.com/docs/integrations/graphs/networkx/
[Principal](https://github.com/milvus-io/bootcamp/blob/master/bootcamp/RAG/advanced_rag/langgraph-graphrag-agent-local.ipynb)
https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/
https://neo4j.com/docs/operations-manual/current/docker/introduction/

[MCP](https://medium.com/data-science-in-your-pocket/rag-mcp-server-tutorial-89badff90c00)
[MCP-LANG](https://docs.langchain.com/oss/python/use-mcp)


Hay como usar buscadores en línea para preguntas aún más específicas y que no estén en el vectordabase o Graph

[WebSearchTool](https://python.langchain.com/docs/integrations/tools/searx_search/)

O también se podría hacer un InMemomryVectorStore para cargar el contexto a la pregunta
[InMemoryVectorStore](https://python.langchain.com/docs/integrations/tools/searx_search/)
Pero mejor sería cargarlo directo a otra base y hacer un ruteador

O la mejor opción es definir un PROMPT para que busque con el proopio LLM
