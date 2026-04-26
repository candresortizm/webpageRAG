from langchain_aws import BedrockEmbeddings
from dotenv import load_dotenv

load_dotenv()

class Embedding:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Creamos el modelo real y lo guardamos como un atributo privado
            cls._instance._model = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
        return cls._instance._model 

    def __getattr__(self, name):
        """
        Cualquier llamada a un método que no exista en esta clase (ej. .embed_query)
        se redirigirá automáticamente a _model.
        """
        return getattr(self._model, name)