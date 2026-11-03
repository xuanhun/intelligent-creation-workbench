"""Read-only bootstrap probes. No credentials or external connections."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from creation_workbench import __version__


class Capabilities(BaseModel):
    schema_version: str = "1"
    stage: str = "B00"
    version: str = __version__
    runtime_connected: bool = False
    creation_enabled: bool = False
    persistence_enabled: bool = False


def create_app() -> FastAPI:
    application = FastAPI(
        title="智能创作工作台 API",
        version=__version__,
        description="B00 只读开发探针，真实 Runtime 与业务能力尚未接入。",
    )

    @application.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "alive", "version": __version__}

    @application.get("/health/ready", responses={503: {"description": "Runtime unavailable"}})
    def ready() -> JSONResponse:
        return JSONResponse(status_code=503, content={
            "status": "not_ready", "reason": "runtime_not_configured",
        })

    @application.get("/api/v1/capabilities", response_model=Capabilities)
    def capabilities() -> Capabilities:
        return Capabilities()

    return application


app = create_app()
