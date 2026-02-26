from orchestrator.graph import app, state
from memory.queue_manager import buscar_na_fila, salvar_resultado_tarefa
from memory.cache import salvar_resultado
from memory.vector_store import salvar_respostas_vdb

while(True):
    print(f"[Worker] Aguardando novos textos")
    mensagem = buscar_na_fila()
    texto = mensagem.get("texto")
    task_id = mensagem.get("task_id")
    print(f"[Worker] Processando...")

    input_state = state.copy()
    input_state["texto_original"] = texto

    resultado = app.invoke(input_state)

    if not resultado.get("cache_found"):
        salvar_resultado(resultado["texto_padronizado"], resultado) #cache
        salvar_respostas_vdb(resultado) #base de dados vetorial

    if task_id:
        salvar_resultado_tarefa(task_id, resultado)

    print("\n[RESULTADO FINAL]")
    for chave, valor in resultado.items():
        if chave == "embeddings" and isinstance(valor, list): 
            print(f"{chave}: Embeddings de tamanho {len(valor)}")
        elif chave == "contexto_memoria" and isinstance(valor, list):
            print(f"{chave}:")
            for i, item in enumerate(valor, 1):
                print(f"  {i}. {item}")
        else:
            print(f"{chave}: {valor}")