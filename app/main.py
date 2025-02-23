from fastapi import FastAPI
from app.routers import patrons_router, health_check_router, drinks_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse


app = FastAPI()

app.include_router(patrons_router)
app.include_router(health_check_router)
app.include_router(drinks_router)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
async def root():
    """Redirect to the /docs endpoint."""
    return RedirectResponse(url="/docs")
