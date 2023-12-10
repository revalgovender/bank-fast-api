from fastapi import FastAPI
from bank.db import models
from bank import api
from bank.db.database import engine


def create_app():
    app = FastAPI(
        title="Bank",
        description="Technical task",
        version="1.0.0",
        debug=False
    )
    app.include_router(router=api.router, prefix="/api")

    return app


def create_db():
    models.Base.metadata.create_all(bind=engine)
