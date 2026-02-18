"""FastAPI application entry point"""
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.logging_config import setup_logging
from app.api.routes import search, chat

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("InfoCollectorAgent starting up")
    yield
    logger.info("InfoCollectorAgent shutting down")


# Create FastAPI app
app = FastAPI(
    title="InfoCollectorAgent",
    description="AI-powered event discovery platform for local activities",
    version="0.1.0",
    lifespan=lifespan
)


# Include routers
app.include_router(search.router)
app.include_router(chat.router)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred"
            }
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "InfoCollectorAgent",
        "version": "0.1.0",
        "docs": "/docs"
    }
