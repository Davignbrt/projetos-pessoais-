from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(100), nullable=False)
    
    produtos: Mapped[list['Produtos']] = relationship('Produtos', back_populates='usuario')

class Produtos(Base):
    __tablename__ = 'produtos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=False)

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='produtos')
