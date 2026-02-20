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
Sua tarefa é criar uma resposta humana e coesa baseada em múltiplos aspectos analisados.

Dados do Processamento:
- Texto Original: {texto_padronizado}
- Lista de Análises: {analise}
- Categorias Atribuídas: {classe}

Instruções:
1. Comece resumindo o sentimento geral do texto.
2. Explique cada categoria atribuída conectando-a com os aspectos correspondentes da análise.
3. Use conectivos de contraste (ex: "Embora você esteja satisfeito com X, notamos sua insatisfação com Y") se houver sentimentos mistos.
4. Se o resultado for "Inconclusivo", explique que a mensagem foi ambígua demais para os critérios de segurança do sistema.
5. Mantenha um tom profissional, mas empático.

Formato de Saída (JSON):
{{
  "explicacao_final": "...",
  "resumo_executivo": "1 linha curta"
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