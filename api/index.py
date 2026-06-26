"""Vercel entrypoint — exports FastAPI app for serverless deployment."""

from app.main import app

__all__ = ["app"]
