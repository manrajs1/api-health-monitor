from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Monitor(BaseModel):
    url : str
    

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/monitors")
def num_monitors():
    return {"message": "There are 5 monitors"}

@app.get("/status")
def status():
    return {"message" : "Status is good"}

@app.post("/monitors")
def add_monitor(monitor: Monitor):
    url = monitor.url
    return url