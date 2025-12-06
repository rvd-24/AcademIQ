# Package initialization for src
# Ensure a compatible event loop policy is set early on Windows so async DB drivers (psycopg) work.
import sys
import asyncio

if sys.platform.startswith("win"):
    try:
        print("Setting WindowsSelectorEventLoopPolicy for asyncio")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
