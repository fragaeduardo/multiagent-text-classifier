import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()

template_classification = ("""
Você é o Agente Classificador Multi-Label.
Sua tarefa é receber uma lista de aspectos analisados e atribuir a categoria correta para CADA UM deles.

Categorias Permitidas:
- SUPORTE_TECNICO: Problemas técnicos ATIVOS, bugs ou dificuldades de acesso AGORA, apenas coisas ainda não resolvidas/respondidas.
- VENDAS: Preços, custos, planos, renovações ou interesse de compra.
- RECLAMACAO: Insatisfação, críticas, demora no atendimento ou serviços ruins.
- ELOGIO: Feedbacks positivos e satisfação.
- SPAM: Conteúdo irrelevante, links suspeitos ou lixo eletrônico.
- OUTROS: Assuntos que não se encaixam nas definições acima.

Retorne uma lista de categorias únicas que representam o texto como um todo, baseando-se nos aspectos.

Formato de Saída (JSON):
{{
  "categorias_identificadas": ["CATEGORIA_1", "CATEGORIA_2"],
  "confianca_media": 0.0 a 1.0
}}

Dados para análise:
{lista_de_aspectos}
""")

prompt = PromptTemplate(input_variables=["lista_de_aspectos"], template=template_classification)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6) #verbose=True para ver o que está acontecendo

chain = prompt | llm | parser






def classification (state: dict) -> dict:
    input_analise = state.get("analise")
    print(f"[Agente classificador] Iniciando processamento")

    resultado_json = chain.invoke({"lista_de_aspectos": input_analise})

    if resultado_json.get("confianca_media") < 0.4:
        state["classe"] = "Inconclusivo"
    else: 
        state["classe"] = resultado_json.get("categorias_identificadas")


    return state