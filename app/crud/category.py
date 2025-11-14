from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Category as CategoryModel
from app.schema import Category
from app.crud.base import CRUDBase


class CRUDCategory(CRUDBase[CategoryModel, Category]):
    async def get_detail(self, db: AsyncSession, category_cd: str) -> CategoryModel | None:
        """Fetch survey with related program and survey type."""
        result = await db.execute(
            select(CategoryModel)
            .filter(CategoryModel.category_cd == category_cd)
            .options(
                selectinload(CategoryModel.base_questions),
            )
        )
        return result.scalars().first()


category = CRUDCategory(CategoryModel)
