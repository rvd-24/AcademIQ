import sys
import asyncio

# Ensure this runs only on Windows
if sys.platform.startswith("win"):
    try:
        # Use SelectorEventLoop which is compatible with psycopg async
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        # Be defensive: if setting the policy fails, continue without raising
        pass
