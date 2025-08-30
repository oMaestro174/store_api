# store/controllers/product.py (VERSÃO ATUALIZADA)

from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from pymongo.errors import DuplicateKeyError # Importar o erro específico
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import product_usecase

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: product_usecase = Depends()
) -> ProductOut:
    # ALTERAÇÃO 1: Mapear exceção de inserção (chave duplicada)
    try:
        return await usecase.create(body=body)
    except DuplicateKeyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with name '{body.name}' already exists.",
        )


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: product_usecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    # ALTERAÇÃO 2: Adicionar query params para filtro de preço
    min_price: Optional[float] = Query(None, alias="min_price"),
    max_price: Optional[float] = Query(None, alias="max_price"),
    usecase: product_usecase = Depends()
) -> List[ProductOut]:
    return await usecase.query(min_price=min_price, max_price=max_price)


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: product_usecase = Depends(),
) -> ProductOut:
    # ALTERAÇÃO 3: Capturar exceção de Not Found na controller
    try:
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: product_usecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
