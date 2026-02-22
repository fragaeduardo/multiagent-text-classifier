import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings

MODEL_EMBEDDINGS="text-embedding-3-small"

def config_embeddings() -> OpenAIEmbeddings:

    return OpenAIEmbeddings(model=MODEL_EMBEDDINGS)