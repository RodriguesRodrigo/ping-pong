from threading import Thread

from fastapi import FastAPI

from src import scheduler
from src.api import router
from src.database import init_db


app = FastAPI()
init_db()
app.include_router(router)

@app.on_event("startup")
async def startup_scheduler() -> None:
    scheduler_thread = Thread(target=scheduler.run)
    scheduler_thread.daemon = True
    scheduler_thread.start()
