import os
import shutil
from langchain_chroma import Chroma
from rag.core.embedding_model import Embedding

CHROMA_PATH = "data/chroma"

class VectorDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Creamos el modelo real y lo guardamos como un atributo privado
            cls._instance._db = Chroma(
                                            persist_directory=CHROMA_PATH, embedding_function=Embedding()
                                )
        return cls._instance
    
    @classmethod
    def limpiar_bd(cls):
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
    
    def __getattr__(self, name):
        """
        Cualquier llamada a un método que no exista en esta clase (ej. .get, .add_documents, etc.)
        se redirigirá automáticamente a _model.
        """
        if self._db is None:
            raise AttributeError("La base de datos no está inicializada.")
        return getattr(self._db, name)