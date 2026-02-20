import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()

template_explanation = ("""
Você é o Agente Explicador de um sistema inteligente de classificação.
Sua tarefa é explicar de forma amigável e clara por que o texto foi classificado em uma determinada categoria.

Dados do Processamento:
- Texto Original: {texto_padronizado}
- Análise Semântica: {analise}
- Categoria Atribuída: {classe}

Instruções:
1. Comece confirmando a categoria que o sistema escolheu.
2. Justifique a decisão usando pontos específicos da análise (tom de voz, intenção, tópicos).
3. Se a categoria for "SPAM", explique que o conteúdo foi filtrado por segurança ou relevância.
4. Se a categoria for "Inconclusivo", explique que o sistema não atingiu o grau de certeza necessário para uma classificação segura (devido à ambiguidade ou falta de contexto no texto) e peça gentilmente que o usuário reformule a mensagem de forma mais clara.
5. Mantenha um tom prestativo e profissional.

Formato de Saída (JSON):
{{
  "explicacao_final": "O texto foi classificado como... porque...",
  "resumo_executivo": "1 linha de resumo"
}}
""")

prompt = PromptTemplate(input_variables=["texto_padronizado", "analise", "classe"], template=template_explanation)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4) #verbose=True para ver o que está acontecendo

chain = prompt | llm | parser






def explanation (state: dict) -> dict:
    input_texto = state.get("texto_padronizado")
    input_analise = state.get("analise")
    input_classe = state.get("classe")
    print(f"[Agente explicador] Iniciando processamento")

    resultado_json = chain.invoke(
        {"texto_padronizado": input_texto, 
        "analise": input_analise, 
        "classe": input_classe})

    state["explicacao"] = resultado_json.get("explicacao_final")
    state["resumo_executivo"] = resultado_json.get("resumo_executivo")


    return state