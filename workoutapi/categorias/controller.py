from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException

from sqlalchemy.future import select

from workoutapi.categorias.schemas import CategoriaIn, CategoriaOut
from workoutapi.categorias.models import CategoriaModel

from workoutapi.contrib.dependencies import DatabaseDependency


router = APIRouter()


@router.post(
    "/",
    summary="Criar nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out


@router.get(
    "/",
    summary="Listar categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def get(
    db_session: DatabaseDependency,
) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        (await db_session.execute(select(CategoriaModel))).scalar().all()
    )

    return categorias


@router.get(
    "/{id}",
    summary="Consultar uma categoria por id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id)))
        .scalar()
        .first()
    )

    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com {id=} não encontrada",
        )

    return categoria
