from models.llm import get_llm
llm = get_llm(temperature=0.2)

from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()



template_analysis = ("""
Você é o Agente Analisador. Sua tarefa é decompor o texto em diferentes ASSUNTOS (aspectos) e analisar cada um individualmente.

Para cada assunto identificado, você deve extrair:
1. Assunto: O tema específico (ex: Login, Preço, Interface).
2. Tom de Voz: O tom do usuário sobre esse tema (ex: irritado, satisfeito, neutro).
3. Intenção: O que o usuário pretende (ex: reclamar, elogiar, tirar dúvida).
4. Urgência: O nível de necessidade para esse ponto específico (baixa, média, alta).


Regra de Intenção: Diferencie entre ações concluídas e ações pendentes. (ex: se o usuário cita um bug para reclamar do tempo de resposta, a intenção é 'reclamar', porém se o usuário cita um bug porque precisa de ajuda para resolvê-lo agora, a intenção é 'resolver_problema'
Regra de Sarcasmo: Analise o texto como um todo antes de segmentar. Se houver elogios contradizendo falhas graves (ex: 'parabéns' por um site caído), identifique como Sarcasmo. Nesses casos, o Tom de Voz deve ser 'irônico' e a Intenção deve ser 'reclamar' para todos relacionados a falha.
Formato de Saída (JSON):
{{
  "analise_semantica": [
    {{
      "assunto": "...",
      "tom_de_voz": "...",
      "intencao": "...",
      "nivel_urgencia": "...",
      "trecho_referencia": "..." 
    }}
  ]
}}

Texto para analisar: {texto_padronizado}
""")

prompt = PromptTemplate(input_variables=["texto_padronizado"], template=template_analysis)


chain = prompt | llm | parser


def analysis (state: dict) -> dict:
    input_text = state.get("texto_padronizado")

    print(f"[Agente analisador] Iniciando processamento")

    resultado_json = chain.invoke({"texto_padronizado": input_text})


    state["analise"] = resultado_json.get("analise_semantica")

    return state