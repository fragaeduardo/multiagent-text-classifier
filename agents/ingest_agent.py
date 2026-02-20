from models.llm import get_llm
llm = get_llm(temperature=0.2)

from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()



template_text = ("""
Você é o Agente Ingestor de um sistema de classificação de texto multi-agente.
Sua tarefa é receber um texto bruto, limpá-lo e extrair metadados básicos.

Responsabilidades:
1. Limpeza: Remova espaços em excesso, caracteres especiais desnecessários e quebras de linha redundantes.
2. Normalização: Mantenha o sentido, mas padronize a estrutura básica do texto.
3. Idioma: Detecte o idioma do texto (ex: pt-BR, en-US).
4. Metadados: Calcule o tamanho do texto original e gere um resumo de 1 frase.

Formato de Saída (JSON):
{{
  "texto_padronizado": "...",
  "metadados": {{
    "idioma": "...",
    "tamanho_original": {tamanho},
    "resumo": "..."
  }}
}}
Texto para processar: {text_to_ingest}
""")

prompt = PromptTemplate(input_variables=["text_to_ingest", "tamanho"], template=template_text)

chain = prompt | llm | parser


def ingest (state: dict) -> dict:
    input_text = state.get("texto_original", "")
    input_text = input_text.replace("\n", " ")
    input_text = " ".join(input_text.split())
    input_size = len(input_text)

    print(f"[Agente ingestor] Iniciando processamento")

    resultado_json = chain.invoke({"text_to_ingest": input_text, "tamanho": input_size})

    state["texto_padronizado"] = resultado_json.get("texto_padronizado")
    state["metadados"] = resultado_json.get("metadados")

    return state