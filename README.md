# webpageRAG
Proyecto de un modelo RAG que extrae información de una página web, la guarda en una base de datos vectorial y permite la interacción con la información usando lenguaje natural.

## Ejecución local:

Se recomienda primero la creación de un entorno virtual.

python -m venv env

Activar el entorno virtual:

.\env\Scripts\activate

Instalar las dependencias:

pip install .

Ejecutar el Api:

python .\src\api_handler.py  



## Documentación de referencia consultada:
-https://docs.langchain.com/oss/python/integrations/document_loaders/recursive_url
