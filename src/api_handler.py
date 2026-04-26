import uvicorn
from fastapi import FastAPI
from scripts.extractor import cargar_web_main

app = FastAPI()


@app.get("/cargarWeb")
def cargar_pagina():
    cargar_web_main("https://bbva.com.co")
    return "En progreso"

