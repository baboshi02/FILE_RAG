from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from tortoise import Tortoise
import os
import dotenv
from routers import admin, client, registeration

dotenv.load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL") or ""


@asynccontextmanager
async def startup_shutdown_handler(app: FastAPI) -> AsyncGenerator[None, None]:
    print("🌍 Initializing Database Connection...")
    try:
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={"models": ["models.user"]},
        )
        await Tortoise.generate_schemas()
        print("✅ DB connection and schema ready.")
    except Exception as e:
        print(f"❌ DATABASE INITIALIZATION FAILED: {e}")
        raise
    yield
    print("💤 Shutting down and closing DB connection...")
    await Tortoise.close_connections()
    print("🚪 Database connections closed.")


app = FastAPI(lifespan=startup_shutdown_handler)
app.include_router(admin.router)
app.include_router(client.router)
app.include_router(registeration.router)
