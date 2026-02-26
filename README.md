# 🚧 WORK IN PROGRESS 🚧
# Multi-Agent Text Classifier

Sistema robusto de classificação de texto multi-agente baseado em **LangChain** e **LangGraph**. O projeto utiliza **Redis** para gerenciamento eficiente de cache e filas de mensagens, garantindo alta performance. O armazenamento vetorial e a recuperação de informações (RAG) são realizados através do **Qdrant**, integrando **OpenAI Embeddings** para análise semântica profunda e memória de longo prazo. O sistema evolui de uma classificação simples para **Aspect-Based Sentiment Analysis (ABSA)**, permitindo uma compreensão granular de sentimentos e intenções.

> [!IMPORTANT]
> **Status do Projeto**: O sistema ainda está incompleto e em desenvolvimento ativo. Confira o Roadmap abaixo para ver o que falta.

## Roadmap / Próximos Passos

As seguintes funcionalidades estão planejadas para as próximas etapas:

- **Containerização com Docker**: Criação de Dockerfiles e docker-compose para facilitar o deploy e a orquestração de todos os serviços de infraestrutura.
- **Persistência em Nuvem**: Transição do banco de dados vetorial de uma instância local para o **Qdrant Cloud** ou servidor remoto.

---

## Agentes Implementados

1.  **Ingestor**: Limpeza e normalização de texto e extração dos metadados.
2.  **Analisador (ABSA)**: Decompõe o texto em aspectos, identificando tom de voz, intenção e urgência para cada trecho.
3.  **Classificador (Multi-Label)**: Atribui múltiplas categorias (Elogio, Reclamação, Suporte, Vendas) baseando-se na análise granular.
4.  **Explicador**: Gera uma narrativa humana e coesa, tratando contrastes e ironias.

## Casos de Teste de Sucesso

### 1. Sarcasmo e Ironia
**Input**: *"Que maravilha de atualização! O sistema ficou tão 'otimizado' que agora ninguém mais consegue logar."*
**Resultado**: O sistema identificou o tom **irônico** e classificou corretamente como **RECLAMACAO** e **SUPORTE_TECNICO**, ignorando o "elogio" falso.

### 2. Multi-Label e Sentimentos Mistos
**Input**: *"O design é incrível, mas o suporte demorou 3 dias."*
**Resultado**:
- `ELOGIO`: Pela interface.
- `RECLAMACAO`: Pela demora do suporte.
- **Explicação**: *"Embora você esteja satisfeito com o design, notamos sua insatisfação com o suporte."*

### 3. Temporariedade e Intenção
**Input**: *"O boleto veio errado mês passado, mas hoje o suporte me ajudou."*
**Resultado**: O sistema diferenciou uma reclamação de evento passado de um pedido de ajuda resolvido, mapeando as intenções corretamente.

## Infraestrutura e Otimização

1. **Memória de Curto Prazo (Cache com Redis)**
   - **Lógica**: Utiliza o hash (SHA256) do texto padronizado como chave.
   - **Eficiência**: Consultas repetidas ignoram o processamento da LLM, retornando o estado completo instantaneamente.
   - **Integração**: Implementado como um nó dedicado no LangGraph para garantir a persistência dos dados recuperados.

2. **Memória de Longo Prazo (Vector Store com Qdrant)**
   - **Lógica**: Armazenamento vetorial para busca semântica e RAG. Atualmente local, com migração planejada para cloud.

3. **Fila de Processamento (Redis Queue)**
   - **Lógica**: Desacoplamento entre input e processamento via workers.

4. **Modularização**
   - **Lógica**: Centralização da configuração da OpenAI em `models/llm.py` para facilitar a escalabilidade e troca de modelos.

5. **API e Orquestração**
   - **FastAPI**: Camada de serviço assíncrona com suporte a Polling (HTTP 202).
   - **Docker (Planejado)**: Padronização do ambiente e orquestração de serviços (App, Redis, Qdrant).

## Tecnologias Utilizadas
- **Python 3.12**
- **LangChain / LangGraph** (Orquestração de Agentes)
- **OpenAI (GPT-4o-mini)** (Inteligência Central)
- **Redis** (Cache, Queue e Persistência)
- **Qdrant** (Vector Database)
- **FastAPI** (Interface Web e Documentação Swagger)
- **Docker** (Em breve - Containerização)

## Como Rodar

O sistema utiliza uma arquitetura de fila (Producer-Consumer). Siga os passos abaixo:

1. **Preparação**:
   - Crie um ambiente virtual: `python -m venv .venv`
   - Ative-o: `source .venv/bin/activate`
   - Instale as dependências: `pip install -r requirements.txt`
   - Configure sua `OPENAI_API_KEY` no arquivo `.env`
   - Certifique-se de ter instâncias de **Redis** e **Qdrant** rodando localmente.

2. **Inicie o Worker**:
   Em um terminal, execute:
   ```bash
   python worker.py
   ```

3. **Inicie a API**:
   Em outro terminal, execute:
   ```bash
   uvicorn api:app --reload
   ```
   Acesse a documentação automática (Swagger) para testar os endpoints (`/classify`: inicia a análise; `/status`: consulta o resultado).

4. **Envie via CLI** (Opcional):
   Se preferir o terminal, utilize:
   ```bash
   python main.py
   ```
