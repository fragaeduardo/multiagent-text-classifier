from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import atexit

from datetime import datetime
from models.llm import MODEL_LLM
from models.embeddings import MODEL_EMBEDDINGS

import os

_client = None
QDRANT_URL = os.getenv("QDRANT_URL")
COLLECTION_NAME = "mensagens_processadas"
def get_client():
    global _client
    if _client is None:
        if QDRANT_URL:
            print(f"[Qdrant] Conectando via URL: {QDRANT_URL}")
            _client = QdrantClient(url=QDRANT_URL)
        else:
            print(f"[Qdrant] Usando armazenamento local")
            _client = QdrantClient(path="./storage/qdrant")



        if not _client.collection_exists(collection_name=COLLECTION_NAME):
            print(f"[Qdrant] Criando nova coleção: {COLLECTION_NAME}")
            _client.create_collection(collection_name=COLLECTION_NAME, 
                                vectors_config = VectorParams(size=1536, distance=Distance.COSINE))
        
    return _client
    

def fechar_banco(): #evita mensagens de limpeza no final da execução
    global _client
    if _client is not None:
        print("[Qdrant] Encerrando conexão com o banco de vetores")
        _client.close()
atexit.register(fechar_banco)


import uuid
def salvar_respostas_vdb(state: dict):
    client = get_client()
    id_atual = str(uuid.uuid4())
    data = datetime.now().isoformat()
    payload = {
        "data": data,
        "modelo_llm": MODEL_LLM,
        "modelo_embeddings": MODEL_EMBEDDINGS,
        "versao_app": "1.0.0",
        "texto": state["texto_padronizado"],
        "metadados": state["metadados"],
        "analise": state["analise"],
        "classe": state["classe"],
        "explicacao": state["explicacao"],
        "resumo_executivo": state["resumo_executivo"]
    }


    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id = id_atual,
                vector = state["embeddings"],
                payload = payload
            )
        ]
    )
    print(f"[Qdrant] Embeddings salvo com sucesso. ID: {id_atual}")

def buscar_parecidos(vetor_busca, limite):
    client = get_client()
    print(f"[Qdrant] Buscando textos parecidos")
    resultados = client.query_points( #usando query_points pq o search tava bugado
        collection_name = COLLECTION_NAME,
        query = vetor_busca,
        limit = limite
    )
    return resultados.points
