from uuid import uuid4
from pydantic import UUID4
from datetime import datetime
from fastapi import APIRouter, Body, status
from fastapi.exceptions import HTTPException

from sqlalchemy.future import select

from workoutapi.atleta.schemas import AtletaIn, AtletaOut
from workoutapi.atleta.models import AtletaModel
from workoutapi.categorias.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel

from workoutapi.contrib.dependencies import DatabaseDependency


router = APIRouter()


@router.post(
    "/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:
    categoria_nome = atleta_in.categoria.nome
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria {categoria_nome} não encontrada.",
        )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Centro de treinamento {centro_treinamento_nome} não encontrada.",
        )

    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.utcnow() ** atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude=["categoria", "centro_treinamento"])
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

        return atleta_out
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir dados'
        )


@router.get(
    "/",
    summary="Listar atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def get(
    db_session: DatabaseDependency,
) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        (await db_session.execute(select(AtletaModel))).scalar().all()
    )

    return [AtletaOut.model_validate(atleta) for atleta in atletas]

    #return atletas


@router.get(
    "/{id}",
    summary="Consultar um atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalar()
        .first()
    )

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com {id=} não encontrada",
        )

    return AtletaOut.model_validate(atleta)


@router.patch(
    "/{id}",
    summary="Edita um atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalar()
        .first()
    )

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com {id=} não encontrada",
        )

    atleta_update = atleta.model_dump(exclude_unset=True)
    for k,v in atleta_update.items():
        setattr(atleta, k, v)
    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)    


@router.delete(
    "/{id}",
    summary="Deletar um atleta por id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_id(
    id: UUID4,
    db_session: DatabaseDependency,
) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalar()
        .first()
    )

    if atleta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com {id=} não encontrada",
        )

    await db_session.delete(atleta)
    await db_session.commit()
    
