from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workoutapi.contrib.models import BaseModel

from workoutapi.atleta.models import AtletaModel

class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')