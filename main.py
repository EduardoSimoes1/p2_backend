from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações do nosso novo módulo modular
from app.database import get_db
from app.schemas import ProductCreate, ProductResponse
from app.services import ProductService

app = FastAPI(title="API de Gerenciamento de Produtos")

@app.get("/produtos", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def listar_produtos(db: Session = Depends(get_db)):
    return ProductService.listar_todos(db)

@app.post("/produtos", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProductCreate, db: Session = Depends(get_db)):
    return ProductService.criar(db, produto)

@app.get("/produtos/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    product = ProductService.buscar_por_id(db, id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return product

@app.delete("/produtos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(id: int, db: Session = Depends(get_db)):
    sucesso = ProductService.deletar(db, id)
    if not sucesso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return