from fastapi import FastAPI

from .router import router

app = FastAPI(
    title="Product API",
    version="1.0.0",
    description="API for accessing product information",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
