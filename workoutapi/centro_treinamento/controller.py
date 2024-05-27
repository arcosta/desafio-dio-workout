from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException

from sqlalchemy.future import select

from workoutapi.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workoutapi.centro_treinamento.models import CentroTreinamentoModel

from workoutapi.contrib.dependencies import DatabaseDependency


router = APIRouter()


@router.post(
    "/",
    summary="Criar um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )

    db_session.add(centro_treinamento_model)
    await db_session.commit()

    return centro_treinamento_out


@router.get(
    "/",
    summary="Listar centro de treinamentos",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def get(
    db_session: DatabaseDependency,
) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (
        (await db_session.execute(select(CentroTreinamentoModel))).scalar().all()
    )

    return centros_treinamento


@router.get(
    "/{id}",
    summary="Consultar um centro de treinamento por id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalar()
        .first()
    )

    if centro_treinamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de treinamento com {id=} não encontrado",
        )

    return centro_treinamento
