#------------------------------------------------
# Conta Corrente Bancária - FASTAPI
# Gerenciar saldo, depósitos e saques dos clientes
#------------------------------------------------

#IMPORTS ----------------------------------------
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn


#INSTANCE APP ---------------------------------
app = FastAPI(
    title="Conta Corrente Bancária API"
    )


# Adicionar clientes
db_clients = {
    "Joao": 500.00,
    "Maria": 1200.50,
    "Pedro": 300.75,
    "Larissa": 950.00
}

# Criar uma classe para movimentações bancárias: {Saque, Depósito} Obs.: Usar Pydantic
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor da movimentação, deve ser maior que zero")

# Criar um endpoint HOME (raiz).
@app.get("/")
def read_root():
    return {"message": "Conta Bancária API - Conta Corrente"}

# Criar endpoints para consultar saldo.
@app.post("/saldo")
def consultar_saldo(cliente: str):
    if cliente in db_clients:
        return {"message": f"saldo do cliente {cliente} é {db_clients[cliente]}"}
    else:
        return {"error": "Cliente não encontrado"}

# Criar endpoints para realizar saques.
@app.post("/saque")
def consultar_saque(movimentacao: Movimentacao):
    cliente = movimentacao.cliente
    valor = movimentacao.valor
    if cliente in db_clients:
        if db_clients[cliente] >= valor:
            db_clients[cliente] -= valor
            return {"message": f"Saque de {valor} realizado com sucesso. Novo saldo: {db_clients[cliente]}"}
        else:
            return {"error": "Saldo insuficiente para saque"}
    else:
        return {"error": "Cliente não encontrado"}

# Criar endpoints para realizar depósitos.
@app.post("/deposito")
def consultar_deposito(movimentacao: Movimentacao):
    cliente = movimentacao.cliente
    valor = movimentacao.valor
    if cliente in db_clients:
        db_clients[cliente] += valor
        return {"message": f"Depósito de {valor} realizado com sucesso. Novo saldo: {db_clients[cliente]}"}
    else:
        return {"error": "Cliente não encontrado"}

#RUN SERVER -----------------------------------
if __name__ == "__main__":
    uvicorn.run("Exemple2:app", host="0.0.0.0", port=8000, reload=True)