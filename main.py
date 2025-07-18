from fastapi import FastAPI
from database import create_db_and_table

from routes.heroes import router_heroes
from routes.users import router_user

#Api PATHS
app = FastAPI()
app.title = "Heros Api"

@app.on_event("startup")
def on_startup():
    create_db_and_table
    
app.include_router(router_heroes)
app.include_router(router_user)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
