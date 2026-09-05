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
# Runs during FastAPI startup and shutdown
async def lifespan(app: FastAPI):
    setup_database()
    
    # Starting the scheduler as a background task 
    task = asyncio.create_task(scheduler())
    
    # Everything before yield runs at startup
    # Everything after yield runs during shutdown
    yield
    
    # Stopping the scheduler when the app shuts down
    task.cancel()
    

async def scheduler():
    while True:
        # Waiting 5 minutes without blocking FastAPI from handling other requests
        await asyncio.sleep(300)
        
        # Running checks for all saved monitors
        run_all_checks()

# Creating the FastAPI application and using the lifespan startup/shutdown function
app = FastAPI(lifespan=lifespan)

# Telling FastAPI where the Jinja2 HTML templates are stored
templates = Jinja2Templates(directory="templates")

# Mapping the /static URL path to the static folder for CSS and other static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Creating a Monitor model that expects a URL string
class Monitor(BaseModel):
    url : str

# Home page route
@app.get("/", response_class= HTMLResponse)
# Gwtitng hte current request
def root(request: Request):
    # Getting all saved monitors from the database
    monitors = get_monitors()
    
    # Rendering index.html and passing the monitors as dynamic template data 
    return templates.TemplateResponse(
        request=request, name="index.html", context={"monitors" :monitors}
    )

@app.get("/monitors")
def list_monitors():
    monitors = get_monitors()
    formatted_monitors = []
    
    # Converting each database tuple into a dictionary with clear fields for JSON
    for row in monitors:
        monitor_data = {}
        monitor_data['id'] = row[0]
        monitor_data['url'] = row[1]
        formatted_monitors.append(monitor_data)
    return {"monitors": formatted_monitors }

# Route for viewing the history of one monitor using its dynamic monitor id
@app.get("/monitors/{monitor_id}/history", response_class=HTMLResponse)
def get_monitor_history(request: Request, monitor_id: int):
    
    #  Checking that the monitor exists before trying to show its history
    monitor_record = get_monitor(monitor_id)
    
    # Returning a 404 error if the monitor id does not exist
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Getting all saved check history for this monitor
    history = get_check_history(monitor_id)
    
    # Creating a list that will contain formatted history dictionaries
    formatted_history = []

    # Converting each database row into a dictionary for the HTML template
    for row in history:
        history_data = {}
        history_data['id'] = row[0]
        history_data['monitor_id'] = row[1]
        history_data['status_code'] = row[2]
        history_data['response_time'] = row[3]
        
        # Converting the stored timestamp string back into a datetime object
        timestamp = datetime.datetime.fromisoformat(row[4])
        # Converting the UTC timestamp to Pacific Time for display
        timestamp = timestamp.astimezone(ZoneInfo("America/Los_Angeles"))
        # Formatting the datetime into a readable string
        history_data['timestamp'] = timestamp.strftime("%b %d, %Y %I:%M %p")
        
        history_data['up'] = row[5]
        history_data['error'] = row[6]
        
        # Adding the formatted check to the history list
        formatted_history.append(history_data)
        
    # Rendering history.html and passing the history data to the template.
    # request is the current browser request that TemplateResponse uses while building the page
    return templates.TemplateResponse(
        request=request, name="history.html", context={"history" : formatted_history}
    )

# API route to delete a monitor by id
@app.delete("/monitors/{monitor_id}")
def delete_monitor_route(monitor_id: int):
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    delete_monitor(monitor_id)
    
    # Returning a JSON response for API users
    return {"message": f"successfully deleted {monitor_id}"}

# API route to create a monitor using JSON data
@app.post("/monitors")
def create_monitor(monitor: Monitor):
    url = monitor.url
    
    # Rejecting URLs that are not valid public HTTP/HTTPS URLs
    if validate_url(url) is False:
        raise HTTPException(status_code=400, detail="Only public HTTP and HTTPS URLs are allowed")
    
    # Adding the monitor, checking it, and saving the first result
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

# Browser form route to create a monitor 
@app.post("/monitors/create")
def create_monitor_form(request: Request, url:str = Form(...)):
    # Showing the dashboard again with an error if the URL is invalid
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
    
    # Redirecting back to the home page after the form is submitted
    return RedirectResponse("/", status_code=303)

# Browser form route to delete a monitor
@app.post("/monitors/{monitor_id}/delete")
def delete_monitor_form(monitor_id: int):
    monitor_record = get_monitor(monitor_id)
    if monitor_record is None:
        raise HTTPException(status_code=404, detail="Monitor not found")
    delete_monitor(monitor_id)
    return RedirectResponse("/", status_code=303)

# Running a new check for every saved monitor
def run_all_checks():
    monitors = get_monitors()
    for monitor_id, url in monitors:
        
        # Validating the URL again before each automatic request
        if validate_url(url):
            result = request_check(url)
            save_check(monitor_id, result)
        else:
            # Saving a failed result if the URL no longer passes validation
            result = {
                "status_code": None,
                "response_time": 0,
                "up": False,
                "error": "URL validation failed"
            }
            save_check(monitor_id, result)