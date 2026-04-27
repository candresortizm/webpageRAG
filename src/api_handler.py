from fastapi import FastAPI, HTTPException
from rag.core.modelo_mensaje import QueryResponse, SubmitQueryRequest
from rag.core.recuperador import query_rag, obtener_historial
from scripts.extractor import cargar_web_main

app = FastAPI()



@app.get("/cargarWeb")
def cargar_pagina():
    cargar_web_main("https://bbva.com.co")
    return "En progreso"

@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    # Create the query item, and put it into the data-base.
    # Make a synchronous call to the worker (the RAG/AI app).
    query_response = query_rag(request)
 
    return query_response

@app.get("/history/{chat_id}")
def get_history(chat_id: str):
    try:
        history = obtener_historial(chat_id)
        return {"conversation_id": chat_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

