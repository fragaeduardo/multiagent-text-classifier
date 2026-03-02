import redis 
import json

import os
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
QUEUE_NAME = "fila_pendentes"

TASK_RESULT_PREFIX = "task_result:"

def enviar_para_fila(texto, task_id=None):
    mensagem={"texto": texto, "task_id": task_id}

    r.lpush(QUEUE_NAME, json.dumps(mensagem))
    print(f"[Queue] Texto computado com sucesso")

def buscar_na_fila():
    resultado = r.brpop(QUEUE_NAME, timeout=0)

    return json.loads(resultado[1])

def salvar_resultado_tarefa(task_id, resultado):
    chave = f"{TASK_RESULT_PREFIX}{task_id}"
    r.set(chave, json.dumps(resultado), ex=900)

def obter_resultado_tarefa(task_id):
    chave = f"{TASK_RESULT_PREFIX}{task_id}"
    dados = r.get(chave)
    if dados:
        return json.loads(dados)
    else:
        return None
        