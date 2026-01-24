"""
Graceful shutdown procedures
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from ..services.database import engine
from sqlmodel import Session

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown procedures
    """
    logger.info("Starting up the application...")
    
    # Startup procedures
    # Initialize database connection
    with Session(engine) as session:
        # Verify database connectivity
        session.exec("SELECT 1")
    
    logger.info("Database connection verified")
    
    # Initialize MCP server
    from ...mcp.server import get_mcp_server
    mcp_server = get_mcp_server()
    logger.info("MCP server initialized")
    
    yield  # Application runs here
    
    # Shutdown procedures
    logger.info("Shutting down the application...")
    
    # Close database engine
    engine.dispose()
    logger.info("Database engine disposed")

def register_shutdown_handler(app: FastAPI):
    """
    Register shutdown handlers for the application
    """
    app.router.lifespan_context = lifespan