import asyncio
import re
from logging import Logger

from config import SYSTEM_PROMPT
from llm.ollama_configs import (
    FixedOllama,
    PROMPT_TEMPLATE,
)


async def question_generator(
    logger: Logger,
    llm: FixedOllama,
    user_prompt: str,
    docs: str,
    topic: str,
) -> str:
    """
    ollama model prompt and respond
    :param logger: process logger
    :param llm: Ollama model with configs
    :param user_prompt: prompt for question generating
    :param docs: spec docs
    :param topic: topic of question
    :return: model's response
    :raise Exeption: if we got error in Ollama work
    """
    try:
        prompt = PROMPT_TEMPLATE.format(
            system=SYSTEM_PROMPT,
            docs=docs,
            topic=topic,
            user=user_prompt
        )
        logger.info("generator: prompt=%r", prompt.replace("\n", "\\n"))
        # Answer generation
        response_obj = await asyncio.to_thread(lambda: llm.complete(prompt))
        text = getattr(response_obj, "text", None) or getattr(response_obj.message, "content", str(response_obj))
        logger.info("generator: got response text=%r", text)
        # final respond without thinking of model
        response = re.sub(r'(?s)^<think>.*?</think>\s*', '', text)
        logger.info("final_response=%r", response)
        return response
    except Exception as e:
        logger.error(f"Failing in model respond generation: {e}")
        raise
