from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.responses import JSONResponse

from database.connection import get_session
from database.models import User, Product
from src.auth.auth import get_current_active_user
from src.game.repository.game import GameRepository
from src.products.application.products import ProductService
from src.products.dtos.dtos import CreateProductReq
from src.products.repository.products import ProductRepository

product_router = APIRouter(
    tags=["Product"],
)


@product_router.post("/")
async def create_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    req: CreateProductReq,
    session: AsyncSession = Depends(get_session),
):
    """
    상품 생성
    """
    product_service = ProductService(
        product_repository=ProductRepository(session=session),
        game_repository=GameRepository(session=session),
    )
    product = await product_service.create_product(
        title=req.title,
        category_key=req.category_key,
        description=req.description,
        location=req.location,
        latitude=req.latitude,
        longitude=req.longitude,
        game_type=req.game_type,
        max_participants=req.max_participants,
        user_key=current_user.user_key,
        valid_start_time=req.valid_start_time,
        valid_end_time=req.valid_end_time,
    )
    await session.commit()
    return product


@product_router.get("/list")
async def get_products(
    # current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    상품 목록 조회
    """
    product_service = ProductService(
        product_repository=ProductRepository(session=session),
        game_repository=GameRepository(session=session),
    )
    products = await product_service.get_products()
    return products


@product_router.get("/{product_key}")
async def get_product_detail(
    # current_user: Annotated[User, Depends(get_current_active_user)],
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    상품 상세 조회
    """
    product_service = ProductService(
        product_repository=ProductRepository(session=session),
        game_repository=GameRepository(session=session),
    )
    product = await product_service.get_product_detail(product_key=product_key)
    return product


@product_router.delete("/{product_key}/invalid")
async def invalid_product(
    # current_user: Annotated[User, Depends(get_current_active_user)],
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    상품 유효하지 않게 변경
    """
    statement = select(Product).where(Product.product_key == product_key)
    results = await session.execute(statement)
    product = results.scalar_one_or_none()
    if not product:
        return JSONResponse(content={"message": "존재하지 않는 상품"}, status_code=400)

    product.is_valid = False
    session.add(product)
    await session.commit()
