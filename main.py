from langgraph.graph import StateGraph, END
from agents.ingest_agent import ingest
from agents.analysis_agent import analysis
from agents.classification_agent import classification
from agents.explanation_agent import explanation

state = {
    "texto_original": None,
    "texto_padronizado": None,
    "metadados": None,
    "analise": None,
    "embeddings": None,
    "contexto_memoria": None,
    "classe": None,
    "explicacao": None
}

def agent_ingestor(state: dict) -> dict:
    return ingest(state)

def agent_analysis(state: dict) -> dict:
    return analysis(state)

def agent_classification(state: dict) -> dict:
    return classification(state)

def agent_explanation(state: dict) -> dict:
    return explanation(state)


graph = StateGraph(dict)

graph.add_node("agent_ingestor", agent_ingestor)
graph.add_node("agent_analysis", agent_analysis)
graph.add_node("agent_classification", agent_classification)
graph.add_node("agent_explanation", agent_explanation)

graph.set_entry_point("agent_ingestor")
graph.add_edge("agent_ingestor", "agent_analysis")
graph.add_edge("agent_analysis", "agent_classification") 
graph.add_edge("agent_classification", "agent_explanation")
graph.add_edge("agent_explanation", END)

app = graph.compile()

input_text = input("Digite o texto a ser analisado: ")
state["texto_original"] = input_text
resultado = app.invoke(state)

print("\n[RESULTADO FINAL]")
for chave, valor in resultado.items():
    print(f"{chave}: {valor}")