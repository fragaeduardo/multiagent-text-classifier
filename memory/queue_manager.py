import redis 
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
QUEUE_NAME = "fila_pendentes"

def enviar_para_fila(texto):
    mensagem={"texto": texto}

    r.lpush(QUEUE_NAME, json.dumps(mensagem))
    print(f"[Queue] Texto computado com sucesso")

def buscar_na_fila():
    resultado = r.brpop(QUEUE_NAME, timeout=0)

    return json.loads(resultado[1])