from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import inventory, calculations
import os

app = FastAPI(
    title="BlueScope Steel Inventory API",
    description="Inventory management system for steel products",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(inventory.router)
app.include_router(calculations.router)

# Mount static files for frontend
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
async def root():
    """Serve the frontend web application"""
    static_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(static_path):
        return FileResponse(static_path)
    return {
        "message": "Welcome to BlueScope Steel Inventory API",
        "docs": "/docs",
        "version": "0.1.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
