from fastapi import FastAPI
from database import create_db_and_table
from fastapi.middleware.cors import CORSMiddleware

from routes.heroes import router_heroes
from routes.users import router_user

# Api PATHS
app = FastAPI()
app.title = "Heros Api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_table()


app.include_router(router_heroes)
app.include_router(router_user)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
