from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Program as ProgramModel
from app.schema import Program, ProgramDetail
from app.crud.base import CRUDBase


class CRUDProgram(CRUDBase[ProgramModel, Program]):
    async def get_detail(self, db: AsyncSession, id: int) -> ProgramModel | None:
        """Get a program with nested surveys, activities, and personnel."""
        result = await db.execute(
            select(ProgramModel)
            .filter(ProgramModel.id == id)
            .options(
                selectinload(ProgramModel.surveys),
                # Uncomment if you implement activities/personnel
                # selectinload(ProgramModel.activities),
                # selectinload(ProgramModel.personnel),
            )
        )
        return result.scalars().first()


program = CRUDProgram(ProgramModel)
