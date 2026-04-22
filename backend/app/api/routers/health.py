"""Sağlık kontrol uç noktası."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Sağlık kontrolü")
def health_check():
    """CI/CD ve uptime monitoring için."""
    return {"status": "ok", "service": "emlak-platformu-api"}
