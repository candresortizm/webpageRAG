import os
from langchain_aws import ChatBedrock
from dotenv import load_dotenv

load_dotenv()

BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID")

class ModeloLLM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Creamos el modelo real y lo guardamos como un atributo privado
            cls._instance._model = ChatBedrock(model_id=BEDROCK_MODEL_ID)
        return cls._instance._model 

    def __getattr__(self, name):
        """
        Cualquier llamada a un método que no exista en esta clase (ej. .invoke)
        se redirigirá automáticamente a _model.
        """
        return getattr(self._model, name)