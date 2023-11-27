from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI ()

class Cliente(BaseModel):
    id: int
    nome: str
    data: datetime
    atendimento: str

db_clientes:List [Cliente] = []

@app.get("/fila")
def lista_clientes ():
    if not db_clientes:
        raise HTTPException (status_code=200 , detail="{}")
    return (db_clientes)

@app.get("/fila/{id}")
def posicao_fila (id:int):
    cliente = next((cl for cl in db_clientes if cl.id == id), None)
    if cliente is None:
        raise HTTPException (status_code=404 , detail="Esta posição não existe")
    return(cliente)

@app.post("/fila")
def incluir_cliente (cliente:Cliente):
    if len (cliente.nome) > 20:
        raise HTTPException(status_code=400, detail="O campo nome deve ter no máximo 20 caracteres")
    if cliente.atendimento != "n" and cliente.atendimento != "p":
        raise HTTPException (status_code=400 , detail="O campo tipo de atendimento só aceita 1 caractere n ou p")
    if db_clientes:
        cliente.id=db_clientes[-1].id + 1
        cliente.atendimento = False
    else:
        cliente.id= 1
        cliente.atendimento = False
    db_clientes.append(cliente)
    return "Cliente adicionado"

@app.put("/fila/")
def atualizar_fila ():
    for cliente in db_clientes: 
        cliente.id -= 1
        if cliente.id <= 0:
            cliente.atendimento = True
            cliente.id = 0
        else:
            cliente.atendimento = False

    return "Fila atualizada"

@app.delete("/fila/{id}")
def excluir_cliente(id:int):
    cliente = next((cl for cl in db_clientes if cl.id == id), None)
    if cliente is None:
        raise HTTPException (status_code=404 , detail="Cliente não encontrado")
    db_clientes.remove (cliente) 
    for cliente in db_clientes[id:]:
        cliente.id -= 1
    return "Cliente removido"
