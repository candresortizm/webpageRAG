from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

PROMPT_TEMPLATE = """
Eres un asistente para la respuesta de preguntas sobre los servicios del banco BBVA.
Usa únicamente los siguientes documentos para responder la pregunta.
Si no sabes la respuesta, dí que no la sabes y si tienes sugerencias preséntalas.
Se amable, recuerda que eres un asistente.
Sé muy conciso con la respuesta y házlo en español:
Documentos: {context}
Respuesta:
"""

HISTORY_PROMPT_TEMPLATE = """
Dado un historial de chat y la última pregunta del usuario que podría hacer referencia al contexto del historial de chat o no,
Si la pregunta está relacionada con el historial NO responda la pregunta,
sólo formule una pregunta independiente que pueda entenderse sin el historial de chat.
Si no está relacionada con mensajes anteriores sólo responda la pregunta.
"""

@dataclass
class QueryResponse:
    query_text: str
    response_text: str
    sources: List[str]

class SubmitQueryRequest(BaseModel):
    query_text: str
    chat_history: list[tuple[str, str]]
    conversation_id: str