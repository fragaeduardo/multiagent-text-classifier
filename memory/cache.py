from redis import Redis
import hashlib
import json

import os
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client= Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def gerar_chave(texto):
    return hashlib.sha256( texto.encode() ).hexdigest() #hash pra transformar o texto em assinatura unica de 64 caracteres
    
def get_cache_text(texto):
    print(f"[Cache] Iniciando processamento do cache")
    key = gerar_chave(texto)
    resultado = redis_client.get(key)

    if resultado: 
        print("[Cache] Resultado anterior encontrado")
        return json.loads(resultado)
    else:
        print("[Cache] Resultado anterior não encontrado")
        return None

def salvar_resultado(texto, resultado):
    key = gerar_chave(texto)
    resultado_json = json.dumps(resultado)
    redis_client.set(key, resultado_json, ex=3600) #mantém o resultado só por 1h