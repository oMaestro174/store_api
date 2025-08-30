# store/schemas/product.py (VERSÃO ATUALIZADA)

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional
from bson import Decimal128
from pydantic import AfterValidator, Field
from store.schemas.base import BaseSchema, OutSchema


class ProductBase(BaseSchema):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(True, description="Product status")


class ProductIn(ProductBase, OutSchema):
    ...


class ProductOut(ProductIn):
    ...


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchema):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    # ALTERAÇÃO: Permitir que updated_at seja modificado opcionalmente
    updated_at: Optional[datetime] = Field(None, description="Product update timestamp")


class ProductUpdateOut(ProductOut):
    ...
