from bs4 import BeautifulSoup
import re, os
from dotenv import load_dotenv
from langchain_community.document_loaders import RecursiveUrlLoader

load_dotenv()

PAGINA_WEB_EXTRAER = os.environ.get("PAGINA_WEB_EXTRAER", "https://google.com.co")

# Método principal que se encarga de cargar la página web, extraer su contenido y guardarlo en archivos txt.
def cargar_web_main(url_string: str):
    try:
        documents = cargar_web(url_string)
        guardar_txt(documents)
        print("Finalizado")
    except Exception as e:
        print("Se presentóuna excepción", e)
    
#Cargar recursivamente la documentación
def cargar_web(url_string, profundidad=2):
    try:
        print("URL---->",url_string)
        cargar_documentos = RecursiveUrlLoader(url_string,extractor=bs4_extractor,max_depth=profundidad,encoding='utf-8')
        documents = cargar_documentos.load()
        documents = [
                    doc for doc in documents 
                    if not doc.metadata['source'].lower().endswith('.json')
                ]
        return documents
    except Exception as e:
        print("Se presentóuna excepción", e)

#Extractor para extraer el texto plano del HTML
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for elementos_quitar in soup.find_all(["header", "nav", "footer", "aside"]):
        elementos_quitar.decompose()
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

def guardar_txt(documentos):
    try:
        directory = "data/texto/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for documento in documentos:
            # Crea el archivo txt
            nombre_archivo = documento.metadata["source"].replace("https://","").replace("/","_").replace(".","-")+".txt"
            if len(nombre_archivo) > 90:
                nombre_archivo = nombre_archivo[:90]
            file = open(directory+nombre_archivo, "w", encoding='utf-8')
            file.write(documento.page_content)
            file.write("\n")
            file.close()
    except Exception as e:
        print("Se presentóuna excepción", e)

# Si se llama desde la consola, se ejecuta el método cargar_web_main con la URL definida en el archivo .env
if __name__ == "__main__":
    cargar_web_main(PAGINA_WEB_EXTRAER)