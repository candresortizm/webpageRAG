from dataclasses import dataclass
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from rag.core.database import VectorDatabase
from rag.core.llm_model import ModeloLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from rag.core.modelo_mensaje import  PROMPT_TEMPLATE, QueryResponse

def rag_chain():
    model = ModeloLLM()
    vectorstore = VectorDatabase()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    qa_prompt = ChatPromptTemplate(
        [
            ("system", PROMPT_TEMPLATE),
            ("human", "{input}"),
        ]
    )

    combine_docs_chain = create_stuff_documents_chain(model, qa_prompt)

    qa_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return qa_chain


def query_rag(query_object) -> QueryResponse:
    rag_response = rag_chain()

    response = rag_response.invoke({
        "input": query_object.query_text
    })
    response_text = response["answer"]
    results = response["context"]

    sources = [doc.metadata.get("id", None) for doc in results]
    print(f"Response: {response_text}\nSources: {sources}")

    return QueryResponse(
        query_text=query_object.query_text, response_text=response_text, sources=sources
    )
