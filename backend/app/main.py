import logging

from app.application_factory import create_app

app = create_app()
log = logging.getLogger("uvicorn")


@app.on_event("startup")
async def startup_event():
    """Inits the database on startup"""
    log.info("Starting application")
    # init_db


@app.on_event("shutdown")
async def shutdown_event():
    """logs on shutdown"""
    log.info("Shutting down")
