import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()



template_analysis = ("""
Você é o Agente Analisador de um sistema de classificação de texto.
Sua tarefa é realizar uma decomposição lógica e semântica do texto fornecido.

Responsabilidades:
1. Tom de Voz: Identifique o tom (ex: formal, agressivo, confuso, urgente, amigável).
2. Intenção: Identifique qual é o objetivo principal do usuário (ex: pedido de ajuda, reclamação, dúvida técnica, elogio).
3. Tópicos: Liste os 3 principais assuntos/palavras-chave citados no texto.
4. Urgência: Avalie se o texto demonstra uma necessidade imediata (baixa, média ou alta).

Formato de Saída (JSON):
{{
  "analise_semantica": {{
    "tom_de_voz": "...",
    "intencao_principal": "...",
    "topicos": ["...", "...", "..."],
    "nivel_urgencia": "..."
  }}
}}

Texto para analisar: {texto_padronizado}
""")

prompt = PromptTemplate(input_variables=["texto_padronizado"], template=template_analysis)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4) #verbose=True para ver o que está acontecendo

chain = prompt | llm | parser


def analysis (state: dict) -> dict:
    input_text = state.get("texto_padronizado")

    print(f"[Agente analisador] Iniciando processamento")

    resultado_json = chain.invoke({"texto_padronizado": input_text})


    state["analise"] = resultado_json.get("analise_semantica")

    return state