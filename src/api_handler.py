import uvicorn
from fastapi import FastAPI
from rag.extractor import load_web_main

app = FastAPI()


@app.get("/cargarWeb")
def cargar_pagina():
    load_web_main("https://bbva.com.co")
    return "En progreso"

