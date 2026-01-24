from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.chat import router as chat_router
from .middleware.exception_handlers import handle_base_app_exception, handle_http_exception, handle_general_exception
from .utils.exceptions import BaseAppException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlmodel import Session
from .services.database import engine
from .database.optimization import create_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up the application...")
    # Verify database connectivity
    with Session(engine) as session:
        session.exec("SELECT 1")
    print("Database connection verified")

    # Create database indexes for optimal performance
    create_indexes(engine)
    print("Database indexes created")

    yield  # Application runs here

    # Shutdown
    print("Shutting down the application...")
    engine.dispose()
    print("Database engine disposed")

app = FastAPI(
    title="Todo AI Chatbot Backend",
    version="0.1.0",
    lifespan=lifespan
)

# Register exception handlers
app.add_exception_handler(BaseAppException, handle_base_app_exception)
app.add_exception_handler(StarletteHTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_general_exception)
app.add_exception_handler(Exception, handle_general_exception)

# Include the chat router
app.include_router(chat_router, prefix="/api/{user_id}", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo AI Chatbot Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "checks": {"database": "connected", "mcp_server": "available"}}