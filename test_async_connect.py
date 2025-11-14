import pytest
from sqlalchemy import text
from app.db import engine


@pytest.mark.asyncio
async def test_conn():
    """Simple connectivity smoke test - executed by pytest with asyncio support."""
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        # result may be a ResultProxy; ensure we can fetch rows
        assert result is not None
        _ = result.all()