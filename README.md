# auto-spec-questions
Generation of questions based on your own documents using Ollama models.

## Schema
.
├── main.py                 # Main entry point of the application
├── config.py               # Global configuration parameters (model settings, paths, etc.)
├── utils.py                # Utility functions (logging, file handling, text processing)
│
└── llm/                    # Modules for working with LLM via Ollama
    ├── ollama_configs.py   # Configuration for Ollama connection (host, model, timeout)
    └── ollama_inference.py # Logic for sending prompts and processing responses

## Essential Programs

### Ollama
[Installation guide](https://apxml.com/courses/getting-started-local-llms/chapter-4-running-first-local-llm/setting-up-ollama)

### Tesseract
[Installation guide](https://builtin.com/articles/python-tesseract)

## Installation

```bash
git clone https://github.com/GoodchildTrevor/spec-question-generator.git
cd spec-question-generator
pip install -r requirements.txt
```

## Usage

Add the path to your document and your topic in the `.env` file. Then run `main.py` to generate questions.
