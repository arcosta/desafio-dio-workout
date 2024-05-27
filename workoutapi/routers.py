from fastapi import APIRouter
from workoutapi.atleta.controller import router as atleta_router
from workoutapi.categorias.controller import router as categoria_router
from workoutapi.centro_treinamento.controller import router as centro_treinamento_router


router = APIRouter()

router.include_router(atleta_router, prefix='/atletas', tags=['atletas/'])
router.include_router(categoria_router, prefix='/categoria', tags=['categoria/'])
router.include_router(centro_treinamento_router, prefix='/centro_treinamento', tags=['centro_treinamento/'])