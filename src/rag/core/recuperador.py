from dataclasses import dataclass
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain.prompts import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage
from rag.componentes.database import VectorDatabase
from rag.componentes.historial_db import DatabaseManager
from rag.componentes.llm_model import ModeloLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from rag.core.modelo_mensaje import  HISTORY_PROMPT_TEMPLATE, PROMPT_TEMPLATE, QueryResponse

#Creación de la cadena RAG, que se encargará de procesar las consultas del usuario, recuperar la información relevante de la base de datos vectorial y generar una respuesta utilizando el modelo de lenguaje.
def rag_chain():
    model = ModeloLLM()
    db = VectorDatabase()
    condense_question_prompt = ChatPromptTemplate(
        [
            ("system", HISTORY_PROMPT_TEMPLATE),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    #Si la pregunta está relacionada con mensajes anteriores se reformula la pregunta para que el modelo de lenguaje pueda entender el contexto de la conversación.
    history_aware_retriever = create_history_aware_retriever(
                                    model, db.as_retriever(search_type="similarity", search_kwargs={"k": 5}), condense_question_prompt
                                )

    qa_prompt = ChatPromptTemplate(
        [
            ("system", PROMPT_TEMPLATE),
            ("human", "{input}"),
        ]
    )
    qa_chain = create_stuff_documents_chain(model, qa_prompt)
    convo_qa_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    return convo_qa_chain

def formatear_historial(chat_history, len_history=6):
    formatted_history = []
    if len(chat_history) > 0:
        for human, ai in chat_history[-len_history:]:
            formatted_history.append(HumanMessage(content=human))
            formatted_history.append(AIMessage(content=ai))
        return formatted_history
    else:
        return chat_history


def query_rag(query_object) -> QueryResponse:
    db_history = DatabaseManager().get_history(query_object.conversation_id)
    
    chat_formatted = formatear_historial(db_history)

    rag_response = rag_chain()

    response = rag_response.invoke({
        "input": query_object.query_text,
        "chat_history": chat_formatted,
    })
    
    response_text = response["answer"]
    results = response["context"]
    sources = [doc.metadata.get("id", None) for doc in results]

    DatabaseManager().save_message(query_object.conversation_id, query_object.query_text, response_text)

    return QueryResponse(
        query_text=query_object.query_text, 
        response_text=response_text, 
        sources=sources
    )

def obtener_historial(conversation_id: str) -> list[tuple[str, str]]:
    db_history = DatabaseManager().get_history(conversation_id)
    chat_formatted = formatear_historial(db_history)
    return chat_formatted