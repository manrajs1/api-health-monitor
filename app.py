from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from url_monitoring import request_check, validate_url
from database_operations import add_monitor, save_check, get_check_history, get_monitors, delete_monitor, get_monitor
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
from contextlib import asynccontextmanager
import datetime
from zoneinfo import ZoneInfo
from database_setup import setup_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    task = asyncio.create_task(scheduler())
    yield
    task.cancel()
    
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class Monitor(BaseModel):
    url : str

@app.get("/", response_class= HTMLResponse)
def root(request: Request):
    monitors = get_monitors()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"monitors" :monitors}
    )

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

@app.get("/monitors/{monitor_id}/history", response_class=HTMLResponse)
def get_monitor_history(request: Request, monitor_id: int):
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
        timestamp = datetime.datetime.fromisoformat(row[4])
        timestamp = timestamp.astimezone(ZoneInfo("America/Los_Angeles"))
        history_data['timestamp'] = timestamp.strftime("%b %d, %Y %I:%M %p")
        history_data['up'] = row[5]
        history_data['error'] = row[6]
        formatted_history.append(history_data)
    return templates.TemplateResponse(
        request=request, name="history.html", context={"history" : formatted_history}
    )

@app.delete("/monitors/{monitor_id}")
def delete_monitor_route(monitor_id: int):
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    delete_monitor(monitor_id)
    return {"message": f"successfully deleted {monitor_id}"}

@app.post("/monitors")
def create_monitor(monitor: Monitor):
    url = monitor.url
    if validate_url(url) is False:
        raise HTTPException(status_code=400, detail="Only public HTTP and HTTPS URLs are allowed")
    monitor_record = add_monitor(url)
    result = request_check(url)
    save_check(monitor_record['id'], result)
    return {"monitor_id" : monitor_record['id'],
            "status_code" : result['status_code'],
            "response_time" : result['response_time'],
            "url" : url,
            "up" : result['up'],
            "error": result['error']
            }
    
@app.post("/monitors/create")
def create_monitor_form(request: Request, url:str = Form(...)):
    if validate_url(url) is False:
        monitors = get_monitors()
        return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context={
            "monitors": monitors,
            "error": "Please enter a valid public HTTP or HTTPS URL."
        }    
    )
    monitor_record = add_monitor(url)
    result = request_check(url)
    save_check(monitor_record['id'], result)
    return RedirectResponse("/", status_code=303)

@app.post("/monitors/{monitor_id}/delete")
def delete_monitor_form(monitor_id: int):
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    delete_monitor(monitor_id)
    return RedirectResponse("/", status_code=303)

def run_all_checks():
    monitors = get_monitors()
    for monitor_id, url in monitors:
        if validate_url(url):
            result = request_check(url)
            save_check(monitor_id, result)
        else:
            result = {
                "status_code": None,
                "response_time": 0,
                "up": False,
                "error": "URL validation failed"
            }
            save_check(monitor_id, result)
            
async def scheduler():
    while True:
        await asyncio.sleep(300)
        run_all_checks()
        