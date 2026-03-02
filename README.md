# Multi-Agent Text Classifier

Sistema robusto de classificação de texto multi-agente baseado em **LangChain** e **LangGraph**. O projeto utiliza **Redis** para gerenciamento eficiente de cache e filas de mensagens, garantindo alta performance. O armazenamento vetorial e a recuperação de informações (RAG) são realizados através do **Qdrant**, integrando **OpenAI Embeddings** para análise semântica profunda e memória de longo prazo. O sistema evolui de uma classificação simples para **Aspect-Based Sentiment Analysis (ABSA)**, permitindo uma compreensão granular de sentimentos e intenções.

---

## Arquitetura e Fluxo (Polling)

O sistema utiliza uma arquitetura assíncrona para garantir que a API nunca trave. O fluxo segue o padrão Producer-Consumer:

```text
                [ Usuário ]
                     |
                     | 1. (POST /classify)
                     v
                [ FastAPI ] ------2. (Retorna Task ID)------> [ Usuário ]
                     |
                     | 3. (LPUSH Task)
                     v
                [ Redis Queue ]
                     |
                     | 4. (BRPOP Worker)
                     v
                [ Worker.py ]
                     |
                     | 5. (Inicia Grafo)
                     v
+-------------------------------------------------------------+
|                  ORQUESTRAÇÃO (LangGraph)                   |
|                                                             |
|             6. [ Ingestor ]                                 |
|                     |                                       |
|                     v                                       |
|  7./------------ Texto repetido? -----------\               |
|    |                                        |               |
|  [ SIM ]                                  [ NÃO ]           |
|    |                                        |               |
|    |                                        v               |
|    |                                  8. [ Embeddings ]     |
|    |                                        |               |
|    |                                        v               |
|    |                                  9. [ Qdrant RAG ]     |
|    |                                        |               |
|    |                                        v               |
|    |                                  10. [ Análise ]       |
|    |                                        |               |
|    |                                        v               |
|    |                                  11. [ Classificação ] |
|    |                                        |               |
|    v                                        v               |
|  [ FIM ] <------- (Resultado) ------- 12. [ Explicação ]    |
|                                                             |
+-------------------------------------------------------------+
                     |
                     v
                [ 13. Worker Finaliza ]
                     |
                     |-- 14. (Salva Cache) ----> [ Redis ]
                     |-- 15. (Salva Vetor) ----> [ Qdrant ]
                     \-- 16. (Salva Task)  ----> [ Redis ]


        [ Polling: User -> API (GET /status) -> Redis ]
```

---

## Agentes Implementados

1.  **Ingestor**: Responsável pela limpeza, padronização e normalização do texto bruto, além de extrair metadados técnicos.
2.  **Analisador (ABSA)**: Realiza a análise de sentimento baseada em aspectos. Identifica o tom de voz (ex: sarcasmo), a intenção real e o nível de urgência.
3.  **Classificador (Multi-Label)**: Atribui múltiplas categorias (Elogio, Reclamação, Suporte, Vendas) de forma inteligente, garantindo que não existam duplicatas.
4.  **Explicador**: Gera uma narrativa humana e coesa, criando um **Resumo Executivo** que justifica as decisões tomadas pelos agentes anteriores.

---

## Infraestrutura e Otimização

1. **Memória de Curto Prazo (Cache com Redis)**
   - Utiliza hash SHA256 do texto padronizado. Consultas repetidas são retornadas instantaneamente, economizando tokens e tempo.
2. **Memória de Longo Prazo (Vector Store com Qdrant)**
   - Armazenamento vetorial para busca semântica. Utiliza `text-embedding-3-small` da OpenAI para permitir que o sistema "lembre" de contextos similares.
3. **Fila de Processamento (Redis Queue)**
   - Desacoplamento total via `LPUSH/BRPOP`, possibilitando escala horizontal (múltiplos workers).
4. **API FastAPI**
   - Camada de serviço moderna, assíncrona, com documentação automática via Swagger/OpenAPI.
5. **Containerização (Docker)**
   - Orquestração completa de serviços (App, Redis, Qdrant) garantindo que o ambiente seja idêntico em qualquer máquina.

## Tecnologias Utilizadas
- **Python 3.10+**
- **LangChain / LangGraph** (Orquestração agêntica)
- **OpenAI (GPT-4o-mini)** (Inteligência Central)
- **Redis 8.6+** (Cache e Mensageria)
- **Qdrant** (Banco Vetorial)
- **FastAPI** (Interface Web)
- **Docker & Docker Compose** (Infraestrutura)

---

## Como Executar

### 1. Via Docker (Recomendado)
A forma mais simples de subir o projeto completo:
```bash
# Clone o projeto e configure o .env com sua OPENAI_API_KEY
docker compose up --build
```
Acesse `http://localhost:8000/docs` para testar.

### 2. Via Local (Manual)
1. Instale as dependências: `pip install -r requirements.txt`
2. Configure o `.env`.
3. Certifique-se de que o Redis e Qdrant estão rodando.
4. Inicie o Worker: `python worker.py`
5. Inicie a API: `uvicorn api:app --reload`

---

## Estrutura do Projeto
```text
multiagent/
├── agents/         # Especialistas (Ingest, Analysis, Classification, Explanation)
├── memory/         # Drivers de persistência (Redis, Qdrant)
├── models/         # Configuração de IA (OpenAI)
├── orchestrator/   # Grafo orquestrador (LangGraph)
├── api.py          # Entradas e saídas (FastAPI)
├── worker.py       # Consumer
└── docker-compose.yml
```
