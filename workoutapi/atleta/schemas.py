from typing import Optional
from pydantic import Field, PositiveFloat

from typing_extensions import Annotated

from workoutapi.contrib.schemas import BaseSchema, OutMixin
from workoutapi.categorias.schemas import CategoriaIn
from workoutapi.centro_treinamento.schemas import CentroTreinamentoAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', examples=['Fulano'], max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', examples=['12345678'], max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', examples=[12])]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', examples=[102])]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', examples=[102])]
    sexo: Annotated[str, Field(description='Peso do atleta', examples=['F'], max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletaIn(Atleta):
    ...

class AtletaOut(Atleta, OutMixin):
    ...

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', examples=['Fulano'], max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', examples=[12])]