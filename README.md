# webpageRAG
Proyecto de un modelo RAG que extrae información de una página web, la guarda en una base de datos vectorial y permite la interacción con la información usando lenguaje natural.

## Ejecución local:

Se recomienda primero la creación de un entorno virtual.

python -m venv env

Activar el entorno virtual:

.\env\Scripts\activate

Instalar las dependencias:

pip install -e .

Ejecutar el Api:

python .\src\api_handler.py  

## Patrones de diseño implementados:
* Singleton: En los archivos database.py, embedding_model.py Para tener una única conexión a la Base de datos
* Proxy: En los archivos database.py, embedding_model.py Para que cuando se haga el llamado de métodos de las clases que no estén declarados a clase explícitamente, entonces llame a los métodos de la clase "real".
* Decorador: En el archivo src/api_handler.py las rutas de FastAPI se añaden usando un decorador @app


## Documentación de referencia consultada:
-https://docs.langchain.com/oss/python/integrations/document_loaders/recursive_url
-https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Embeddings.ipynb
-https://docs.langchain.com/oss/python/langchain/retrieval#2-step-rag
