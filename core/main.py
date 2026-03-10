"""
main.py — FastAPI Application Entry Point
==========================================
This is the skeleton for your agent system.
It does three things on startup:
  1. Loads config from .env
  2. Initialises the Ollama LLM client
  3. Registers all agent routers (placeholders for now)

Run with:
    uvicorn main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

# --------------------------------------------------------------------------
# Core imports — these files must exist before you run this
# core/config.py      → loads .env variables
# core/llm_client.py  → initialises and exposes call_llm()
# --------------------------------------------------------------------------
from core.config import settings
from core.llm_client import init_llm


# --------------------------------------------------------------------------
# Router imports — uncomment each line as you build that agent
# Person 1 owns: program, course, about_course, course_detail routes
# Person 2 owns: module, lesson, assessment routes
# --------------------------------------------------------------------------

# --- Person 1 routes (uncomment when ready) ---
# from routes.program_routes import router as program_router
# from routes.course_routes import router as course_router
# from routes.course_detail_routes import router as course_detail_router

# --- Person 2 routes (uncomment when ready) ---
# from routes.module_routes import router as module_router
# from routes.lesson_routes import router as lesson_router
# from routes.assessment_routes import router as assessment_router


# --------------------------------------------------------------------------
# Lifespan — runs once on startup and once on shutdown
# This is where the LLM client is initialised so it's ready for all routes
# --------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print("Starting up...")
    print(f"  Model    : {settings.model_name}")
    print(f"  Base URL : {settings.ollama_base_url}")

    init_llm()  # creates the AsyncOpenAI client pointed at Ollama
    print("  LLM client initialised successfully.")
    print("Ready. Visit http://localhost:8000/docs to explore the API.")

    yield  # app runs here

    # --- SHUTDOWN ---
    print("Shutting down...")


# --------------------------------------------------------------------------
# App creation
# --------------------------------------------------------------------------
app = FastAPI(
    title="EnumVerse Agent System",
    description="AI-powered educational content generation — built on Ollama",
    version="0.1.0",
    lifespan=lifespan,
)


# --------------------------------------------------------------------------
# Router registration — uncomment each as agents are built
# --------------------------------------------------------------------------

# --- Person 1 ---
# app.include_router(program_router, prefix="/program", tags=["Program"])
# app.include_router(course_router, prefix="/course", tags=["Course"])
# app.include_router(course_detail_router, prefix="/course", tags=["Course Detail"])

# --- Person 2 ---
# app.include_router(module_router, prefix="/module", tags=["Module"])
# app.include_router(lesson_router, prefix="/lesson", tags=["Lesson"])
# app.include_router(assessment_router, prefix="/assessment", tags=["Assessment"])


# --------------------------------------------------------------------------
# Health check — the first thing to test after setup
# GET http://localhost:8000/health
# Expected response: {"status": "ok", "model": "llama3.2", "ollama_url": "..."}
# --------------------------------------------------------------------------
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "model": settings.model_name,
        "ollama_url": settings.ollama_base_url,
    }


# --------------------------------------------------------------------------
# Root route — friendly welcome message
# GET http://localhost:8000/
# --------------------------------------------------------------------------
@app.get("/", tags=["System"])
async def root():
    return {
        "message": "EnumVerse Agent System is running.",
        "docs": "Visit /docs for the interactive API explorer.",
        "health": "Visit /health to confirm LLM config.",
    }