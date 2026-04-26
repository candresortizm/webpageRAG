import uvicorn
from fastapi import FastAPI
from rag.core.modelo_mensaje import QueryResponse, SubmitQueryRequest
from rag.core.recuperador import query_rag
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

