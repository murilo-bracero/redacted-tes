from sqlalchemy import ForeignKey, String, DECIMAL, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Negociacao(Base):
    __tablename__ = "negociacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(255))

    imovel_id: Mapped[int] = mapped_column(ForeignKey("imoveis.id"))
    imovel: Mapped["Imovel"] = relationship(lazy="selectin")

    comprador_id: Mapped[int] = mapped_column(ForeignKey("compradores.id"))
    comprador: Mapped["Comprador"] = relationship(lazy="selectin")

class Imovel(Base):
    __tablename__ = "imoveis"

    id: Mapped[int] = mapped_column(primary_key=True)
    valor: Mapped[float] = mapped_column(DECIMAL(17, 2))
    logradouro: Mapped[str] = mapped_column(String(255))
    cep: Mapped[str] = mapped_column(String(8))
    numero: Mapped[int] = mapped_column(Integer)

class Comprador(Base):
    __tablename__ = "compradores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    historico_credito: Mapped[float] = mapped_column(DECIMAL(5, 2))
    renda_estimada: Mapped[float] = mapped_column(DECIMAL(17, 2))