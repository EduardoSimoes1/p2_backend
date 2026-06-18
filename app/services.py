from sqlalchemy.orm import Session
from app.models import ProductModel
from app.schemas import ProductCreate

class ProductService:
    @staticmethod
    def listar_todos(db: Session):
        return db.query(ProductModel).all()

    @staticmethod
    def criar(db: Session, produto_data: ProductCreate):
        db_product = ProductModel(**produto_data.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def buscar_por_id(db: Session, produto_id: int):
        return db.query(ProductModel).filter(ProductModel.id == produto_id).first()

    @staticmethod
    def deletar(db: Session, produto_id: int) -> bool:
        product = db.query(ProductModel).filter(ProductModel.id == produto_id).first()
        if not product:
            return False
        db.delete(product)
        db.commit()
        return True