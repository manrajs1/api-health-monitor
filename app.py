from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from url_request_check import request_check
from database_operations import add_monitor, save_check, get_check_history, get_monitors, delete_monitor, get_monitor

app = FastAPI()

class Monitor(BaseModel):
    url : str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/monitors")
def list_monitors():
    monitors = get_monitors()
    formatted_monitors = []
    for row in monitors:
        monitor_data = {}
        monitor_data['id'] = row[0]
        monitor_data['url'] = row[1]
        formatted_monitors.append(monitor_data)
    return {"monitors": formatted_monitors }

@app.get("/monitors/{monitor_id}/history")
def get_monitor_history(monitor_id: int):
    # Verify the monitor exists before returning history.
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Item not found")
    history = get_check_history(monitor_id)
    formatted_history = []
    for row in history:
        history_data = {}
        history_data['id'] = row[0]
        history_data['monitor_id'] = row[1]
        history_data['status_code'] = row[2]
        history_data['response_time'] = row[3]
        history_data['timestamp'] = row[4]
        history_data['up'] = row[5]
        history_data['error'] = row[6]
        formatted_history.append(history_data)
    return {"history" : formatted_history}

@app.get("/status")
def status():
    return {"message" : "Status is good"}

@app.delete("/monitors/{monitor_id}")
def delete_monitor_route(monitor_id: int):
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_monitor(monitor_id)
    return {"message": f"successfully deleted {monitor_id}"}

@app.post("/monitors")
def create_monitor(monitor: Monitor):
    url = monitor.url
    monitor_record = add_monitor(url)
    result = request_check(url)
    save_check(monitor_record['id'], result)
    return {"monitor_id" : monitor_record['id'],
            "status_code" : result['status code'],
            "response_time" : result['response time'],
            "url" : url,
            "up" : result['Up'],
            "error": result["Error"]
            }