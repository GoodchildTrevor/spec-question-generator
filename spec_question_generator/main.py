import asyncio
from dotenv import load_dotenv
import logging
from pathlib import Path

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODELS, TIMEOUT, USER_PROMPTS
from utils import file_to_text, save_text_to_file
from llm.ollama_configs import FixedOllama
from llm.ollama_inference import question_generator

load_dotenv()

folder_path = Path(os.getenv("DOC_PATHS"))
topic = os.getenv("TOPIC")

LOG_PATH = "../generator.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.debug(f"folder_path = {folder_path} and topic = {topic}")

docs = list()

for file_path in folder_path.rglob('*'):
    logger.info(f'File_ path: {file_path}')
    file_format = file_path.suffix.lower()
    doc = file_to_text(logger, file_path, file_format)
    docs.append(doc)

logger.info(f"Number of docs: {len(docs)}")
all_texts = "\n".join(docs)
save_text_to_file(all_texts, "../all_docs.doc")


async def main():
    for model in MODELS:
        # Model initialization
        llm = FixedOllama(
            model=model,
            request_timeout=TIMEOUT,
        )
        for prompt_name, prompt in USER_PROMPTS.items():
            questions_result = await question_generator(logger, llm, prompt, all_texts, topic)
            filename = f"{model}_{prompt_name}"
            save_text_to_file(questions_result, filename)


if __name__ == "__main__":
    asyncio.run(main())
