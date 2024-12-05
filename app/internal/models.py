from sqlalchemy import ForeignKey, String, DECIMAL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(255))

    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    property: Mapped["Property"] = relationship(lazy="selectin")

    buyer_id: Mapped[int] = mapped_column(ForeignKey("buyers.id"))
    buyer: Mapped["Buyer"] = relationship(lazy="selectin")

class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(DECIMAL(17, 2))

class Buyer(Base):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True)
    credit_score: Mapped[float] = mapped_column(DECIMAL(5, 2))
    estimated_income: Mapped[float] = mapped_column(DECIMAL(17, 2))