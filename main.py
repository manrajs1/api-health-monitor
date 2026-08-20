from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/monitors")
def num_monitors():
    return {"message": "There are 5 monitors"}

@app.get("/status")
def status():
    return {"message" : "Status is good"}