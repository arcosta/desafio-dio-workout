from typing_extensions import Annotated
from workoutapi.contrib.schemas import BaseSchema
from pydantic import Field, UUID4

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', examples=['CT Queen'], max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', examples=['Rua da Oliveiras, 67'], max_length=60)]
    proprietario: Annotated[str, Field(description='Nome do Dono Centro de Treinamento', examples=['Joao'], max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', examples=['CT Queen'], max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]