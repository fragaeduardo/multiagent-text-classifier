from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import atexit

from datetime import datetime
from models.llm import MODEL_LLM
from models.embeddings import MODEL_EMBEDDINGS
client = QdrantClient(path="./storage/qdrant")

COLLECTION_NAME = "mensagens_processadas"
def inicializar_banco():
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"[Qdrant] Criando nova coleção: {COLLECTION_NAME}")
        client.create_collection(collection_name=COLLECTION_NAME, 
                                vectors_config = VectorParams(size=1536, distance=Distance.COSINE))
    else:
        print(f"[Qdrant] Coleção {COLLECTION_NAME} encontrada")
    

inicializar_banco()

def fechar_banco(): #evita mensagens de limpeza no final da execução
    print("[Qdrant] Encerrando conexão com o banco de vetores")
    client.close()
atexit.register(fechar_banco)


import uuid
def salvar_respostas_vdb(state: dict):
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
    print(f"[Qdrant] Buscando textos parecidos")
    resultados = client.query_points( #usando query_points pq o search tava bugado
        collection_name = COLLECTION_NAME,
        query = vetor_busca,
        limit = limite
    )
    return resultados.points