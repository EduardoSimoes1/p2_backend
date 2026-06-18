from pydantic import BaseModel, Field, field_validator

class ProductBase(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float
    estoque: int = 0
    ativo: bool = True

    @field_validator('nome')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('O nome do produto não pode ser vazio.')
        return v.strip()

    @field_validator('preco')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('O preço deve ser maior que zero.')
        return v

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True