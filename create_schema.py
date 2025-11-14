# Usage: python -m create_schema [--drop-existing]

import asyncio
import argparse
from app.db import engine, Base
from app import models 

async def init_models(drop_existing: bool=False):
    async with engine.begin() as conn:
        if drop_existing:
            # Drop all tables (optional)
            await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        print('Creating tables')
        await conn.run_sync(Base.metadata.create_all)
        print('Done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create DB schema")
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing tables before creating them",
    )
    args = parser.parse_args()

    asyncio.run(init_models(drop_existing=args.drop_existing))
