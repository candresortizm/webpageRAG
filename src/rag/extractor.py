from bs4 import BeautifulSoup
import re, os
from langchain_community.document_loaders import RecursiveUrlLoader
import requests

def load_web_main(url_string: str):
    documents = load_web(url_string)
    guardar_txt(documents)
    # chunks = await split_documents(documents)
    # await add_to_chroma(chunks)
    #query = historial_model.update_item()
    print("Finalizado")

#Cargar recursivamente la documentación
def load_web(url_string, profundidad=2):
    print("URL---->",url_string)
    document_loader = RecursiveUrlLoader(url_string,extractor=bs4_extractor,max_depth=profundidad,encoding='utf-8')
    return document_loader.load()

#Extractor para extraer el texto plano del HTML
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

def guardar_txt(documentos):
    directory = "data/texto/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    for documento in documentos:
        print("DOCUMENTO->")
        print(documento)
        # Crea el archivo txt
        file = open(directory+documento.metadata["source"].replace("https://","").replace("/","_").replace(".","-")+".txt", "w", encoding='utf-8')
        print(str(file))
        file.write(documento.page_content)
        file.write("\n")