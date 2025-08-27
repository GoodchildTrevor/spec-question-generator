from llama_index.llms.ollama import Ollama
from llama_index.core import PromptTemplate

PROMPT_TEMPLATE = PromptTemplate("""
    Системное сообщение:
    {system}

    Документы:
    {docs}
    
    По теме {topic} для работника по инструкции из документа выше
    
    {user}
""".strip())


class FixedOllama(Ollama):
    """
    Ollama class with fixing of some inbox bugs
    """

    def _get_response_token_counts(self, response):
        return None

    def chat(self, messages, **kwargs):
        return super().chat(messages, **kwargs)
