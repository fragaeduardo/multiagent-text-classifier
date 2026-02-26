from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from memory.queue_manager import enviar_para_fila, obter_resultado_tarefa
app = FastAPI()

class Requisicao(BaseModel):
    text: str 

class TaskID(BaseModel):
    task_id: str
    status:str

class Resposta(BaseModel):
    classe: List[str]
    explicacao: str



@app.get("/")
async def home():
    return {"msg": "API Online, utilize POST /classify"}

@app.post("/classify", response_model=TaskID)
async def classificar_msg(request: Requisicao):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Texto vazio")

    task_id = str(uuid.uuid4())
    enviar_para_fila(request.text, task_id)

    return {"task_id": task_id, "status": "Processando..."}



@app.get("/status/{task_id}", response_model=Resposta)
async def obter_resultado_msg(task_id: str):
    resultado = obter_resultado_tarefa(task_id)

    if resultado:
        return resultado
    else:
        raise HTTPException(
            status_code = 202,
            detail = "Solicitação ainda em processamento, tente novamente em alguns instantes."
        )

