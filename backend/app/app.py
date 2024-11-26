import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from routes import get_apps_router
from api.routers import router


def get_application() -> FastAPI:
    application = FastAPI(
        title="PROJECT_NAME",
        debug=True,
        version="1.0.0",
        root_path="/monitoractivity",
    )
    # application.include_router(get_apps_router())

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_application()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def test():
    return {"test": 111}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8888, reload=True)
