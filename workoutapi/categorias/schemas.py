from typing_extensions import Annotated

from workoutapi.contrib.schemas import BaseSchema, OutMixin
from pydantic import Field, UUID4


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', examples=['Scale'], max_length=10)]

#class CategoriaIn(Categoria):
#    ...

class CategoriaOut(CategoriaIn, OutMixin):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]