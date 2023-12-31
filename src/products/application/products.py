from datetime import datetime

from src.game.repository.game import GameRepository
from src.products.dtos.dtos import GameType
from src.products.repository.products import ProductRepository


class ProductService:
    def __init__(
        self, product_repository: ProductRepository, game_repository: GameRepository
    ):
        self.repository = product_repository
        self.game_repository = game_repository

    async def get_products(self):
        """
        상품 목록 조회
        """
        products = await self.repository.get_products()
        return products

    async def get_product_detail(self, product_key: int):
        """
        상품 디테일 조회
        """
        return await self.repository.get_product_detail(product_key=product_key)

    async def create_product(
        self,
        title: str,
        category_key: int,
        description: str,
        location: str,
        latitude: float,
        longitude: float,
        game_type: GameType,
        max_participants: int,
        user_key: int,
        valid_start_time: datetime,
        valid_end_time: datetime,
    ):
        """
        상품 생성
        """
        product = await self.repository.create_product(
            title=title,
            category_key=category_key,
            description=description,
            location=location,
            latitude=latitude,
            longitude=longitude,
            game_type=game_type,
            max_participants=max_participants,
            user_key=user_key,
            valid_start_time=valid_start_time,
            valid_end_time=valid_end_time,
        )
        await self.game_repository.create_game(
            product_key=product.product_key, user_key=user_key
        )
        return product
