from fastapi import FastAPI, HTTPException, status
from app.gateway_pagamento import (
    GatewayPagamentoError,
    GatewayIndisponivelError,
    GatewayTimeoutError
)
from app.schemas import CriarPedidoRequest, Pedido, RespostaProcessamento
from app.service import PedidoService

app = FastAPI(
    title="Serviço de Pedidos e Pagamentos",
    description="API para criação e orquestração de pagamentos integrada com gateway externos", 
    version="1.0.0"
)

service = PedidoService()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok", "service": "servico-pedidos"}

@app.post("/pedidos", reponse_model=RespostaProcessamento, status_code=status.HTTP_201_CREATED)
def criar_pedido(payload: CriarPedidoRequest):
    