# webpageRAG
Proyecto de un modelo RAG que extrae información de una página web, la guarda en una base de datos vectorial y permite la interacción con la información usando lenguaje natural.

## Ejecución local con python:

### Requisitos previos:

- Es necesario tener instalado python, se recomienda 3.13.9 o posterior. 
- Poner las variables de entorno en un archivo .env en la raíz del proyecto (tomar como base el archivo ejemplo.env)

### Configuración del entorno:

Para la interación con el modelo através de la API. Primero se recomienda la creación de un entorno virtual.

```
python -m venv env
```

Activar el entorno virtual:

```
.\env\Scripts\activate
```

Instalar las dependencias:

```
pip install -e .
```
**Nota importante:**
Ya que la base de datos vectorial se encuentra cargada, no es necesaria la ejecución del scraper, generación de txt y el cargue a la BD y es posible hacer la ejecución de la API directamente para preguntar sobre los archivos subidos.

### Para el scrapper y guardar de los txt:

En la variable de entorno PAGINA_WEB_EXTRAER se pone la URL de la web que se quiere cargar, si esa variable no se pone, entonces se carga "https://google.com.co". Se ejecuta el script ubicado en src/scripts/extractor.py

```
python .\src\scripts\extractor.py
```

### Para cargar los txt en la base de datos vectorial:

Se ejecuta el script ubicado en src/scripts/cargarBD.py

```
python .\src\scripts\cargarBD.py
```


### Para ejecutar el Api:

```
fastapi run .\src\api_handler.py 
```

## Ejecución con el Dockerfile:

- Es necesario tener instalado python, se recomienda 3.13.9 o posterior. 
- Poner las variables de entorno en un archivo .env en la raíz del proyecto (tomar como base el archivo ejemplo.env)

Crear la imagen
```
docker build -t web-rag-langchain .
```

Ejecutar la imagen
```
docker run --rm -p 8000:8000 --env-file .env web-rag-langchain
```

## Patrones de diseño implementados:
* **Singleton:** En los archivos database.py, embedding_model.py Para tener una única conexión a la Base de datos
* **Proxy:** En los archivos database.py, embedding_model.py Para que cuando se haga el llamado de métodos de las clases que no estén declarados a clase explícitamente, entonces llame a los métodos de la clase "real".
* **Decorador:** En el archivo src/api_handler.py las rutas de FastAPI se añaden usando un decorador @app

## Futuras mejoras del sistema:
* Implementación de un reranker para mejorar la relevancia de los resultados recuperados antes de pasarlos al LLM.
* Permitir la carga de nuevos datos usando el contenedor.
* Desarrollo de una interfaz frontend para la interacción.

## Uso de herramientas de IA:
* Para la generación del Dockerfile le pedí a copilot que lo creara.
* Uso de Gemini como heramienta para consulta y apoyo en tareas específicas.

**Nota:**
Hace algún tiempo había desarrollado unos proyectos similares que tomé como base.

## Documentación de referencia consultada:
-https://docs.langchain.com/oss/python/integrations/document_loaders/recursive_url
-https://docs.langchain.com/oss/python/langchain/retrieval#2-step-rag
