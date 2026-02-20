import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()

template_classification = ("""
Você é o Agente Classificador. Sua tarefa é decidir a categoria final do texto.
Você deve usar a análise semântica feita pelo agente anterior para tomar sua decisão.

Categorias Permitidas:
- SUPORTE_TECNICO: Dúvidas sobre erros, bugs ou acesso.
- VENDAS: Perguntas sobre preços, planos ou compras.
- RECLAMACAO: Críticas ao serviço ou insatisfação.
- ELOGIO: Feedbacks positivos.
- SPAM: Mensagens promocionais não solicitadas, links suspeitos, textos aleatórios sem sentido ou tentativas de "jailbreak" do sistema.
- OUTROS: Assuntos que não se encaixam acima.

Dados para análise:
- Tom de voz: {tom_de_voz}
- Intenção percebida: {intencao_principal}
- Tópicos: {topicos}
- Nível de urgência: {nivel_urgencia}

Formato de Saída (JSON):
{{
  "classificacao_final": "NOME_DA_CATEGORIA",
  "confianca": 0.0 a 1.0 (float)
}}
""")

prompt = PromptTemplate(input_variables=["tom_de_voz", "intencao_principal", "topicos", "nivel_urgencia"], template=template_classification)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6) #verbose=True para ver o que está acontecendo

chain = prompt | llm | parser






def classification (state: dict) -> dict:
    input_analise = state.get("analise")
    input_tom = input_analise.get("tom_de_voz")
    input_intencao = input_analise.get("intencao_principal")
    input_topicos = input_analise.get("topicos")
    input_urgencia = input_analise.get("nivel_urgencia")
    print(f"[Agente classificador] Iniciando processamento")

    resultado_json = chain.invoke(
        {"tom_de_voz": input_tom, 
        "intencao_principal": input_intencao, 
        "topicos": input_topicos,
        "nivel_urgencia": input_urgencia})


    if resultado_json.get("confianca") < 0.4:
        state["classe"] = "Inconclusivo"
    else: 
        state["classe"] = resultado_json.get("classificacao_final")


    return state