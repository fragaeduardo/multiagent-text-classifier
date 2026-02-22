from langgraph.graph import StateGraph, END
from agents.ingest_agent import ingest
from models.embeddings import config_embeddings
from agents.analysis_agent import analysis
from agents.classification_agent import classification
from agents.explanation_agent import explanation
from memory.vector_store import salvar_respostas_vdb, buscar_parecidos
from memory.queue_manager import enviar_para_fila

from memory.cache import get_cache_text, salvar_resultado

state = {
    "texto_original": None,
    "texto_padronizado": None,
    "cache_found": None,
    "metadados": None,
    "analise": None,
    "embeddings": None,
    "contexto_memoria": None,
    "classe": None,
    "explicacao": None,
    "resumo_executivo": None,
}

def agent_ingestor(state: dict) -> dict:
    return ingest(state)

def agent_analysis(state: dict) -> dict:
    return analysis(state)

def agent_classification(state: dict) -> dict:
    return classification(state)

def agent_explanation(state: dict) -> dict:
    return explanation(state)

def node_check_cache(state: dict) -> dict:
    cache = get_cache_text( state["texto_padronizado"])
    if cache:
        state.update(cache) #sobrescreve os valores no state com os do cache
        state["cache_found"] = True
    else:
        state["cache_found"] = False
    
    return state

def router_cache(state: dict):
    if state.get("cache_found"):
        return "found"
    else:
        return "not found"

def node_generate_embeddings(state:dict) -> dict:
    print("[Embeddings] Iniciando processamento")
    model = config_embeddings()
    embeddings = model.embed_query(state["texto_padronizado"])
    state["embeddings"] = embeddings
    return state

def node_retrieve_context (state:dict) -> dict:
    print("[Qdrant] Recuperando contexto")
    buscas = buscar_parecidos(state["embeddings"], 3)

    contexto_limpo = []
    for item in buscas: 
        texto_antigo = item.payload.get("texto")
        classe_antiga = item.payload.get("classe")
        explicacao_antiga = item.payload.get("explicacao")

        contexto_limpo.append(f"Histórico: {texto_antigo} (Classe atribuida: {classe_antiga}) (Explicação: {explicacao_antiga})")
    
    
    state["contexto_memoria"] = contexto_limpo
    return state



graph = StateGraph(dict)

graph.add_node("agent_ingestor", agent_ingestor)
graph.add_node("node_check_cache", node_check_cache)
graph.add_node("node_generate_embeddings", node_generate_embeddings)
graph.add_node("node_retrieve_context", node_retrieve_context)
graph.add_node("agent_analysis", agent_analysis)
graph.add_node("agent_classification", agent_classification)
graph.add_node("agent_explanation", agent_explanation)

graph.set_entry_point("agent_ingestor")
graph.add_edge("agent_ingestor", "node_check_cache")
graph.add_conditional_edges("node_check_cache", router_cache, {"found": END, "not found": "node_generate_embeddings"})
graph.add_edge("node_generate_embeddings", "node_retrieve_context")
graph.add_edge("node_retrieve_context", "agent_analysis")
graph.add_edge("agent_analysis", "agent_classification") 
graph.add_edge("agent_classification", "agent_explanation")
graph.add_edge("agent_explanation", END)

app = graph.compile()







if __name__ == "__main__":
    input_text = input("Digite o texto a ser analisado: ")
    enviar_para_fila(input_text)