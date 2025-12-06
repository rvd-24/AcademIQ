"""
Simple async DB connection test using the project's async SQLAlchemy engine.
Run with: `python -m src.scripts.test_db`

This script will:
- load environment from `.env` (if present)
- ensure a Selector event loop on Windows
- connect to the async engine in `src.config.database`
- run `SELECT 1` and print the result
"""
import sys
import asyncio
from dotenv import load_dotenv
load_dotenv()

# Ensure compatible event loop on Windows
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

from sqlalchemy import text
from src.config import database

async def main():
    engine = database.engine
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            scalar = result.scalar()
            print("✅ DB connection successful. SELECT 1 ->", scalar)
    except Exception as e:
        print("❌ DB connection failed:", repr(e))
    finally:
        # Dispose engine connections
        try:
            await engine.dispose()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())
