# API Health Monitor

API Health Monitor is a FastAPI web application that allows users to add public HTTP/HTTPS URLs, check whether they are reachable, and view a history of previous checks.

## Features

* Add public URLs to monitor
* Check HTTP status code and response time
* Store check history in SQLite
* Automatically run checks every 5 minutes
* View monitor history in a web dashboard
* Delete monitors and their related history
* Validate URLs and block private, loopback, and other unsafe IP addresses
* Display timestamps in Pacific Time

## Tech Stack

* Python
* FastAPI
* HTTPX
* SQLite
* Jinja2
* HTML/CSS
* Pytest

## How It Works

1. A user adds a URL from the dashboard.
2. The URL is validated before a request is sent.
3. The application sends an HTTP request using HTTPX.
4. The status code, response time, timestamp, reachability, and error information are stored in SQLite.
5. The scheduler checks all saved monitors again every 5 minutes.
6. Users can view previous checks or delete a monitor from the dashboard.

## Running the Project

Install the required Python packages and start the FastAPI application.

Then open the local FastAPI server in your browser.

## Testing

Run the tests with:

```bash
pytest
```

The tests use a temporary SQLite database so the real application database is not modified.

## Notes

A monitor is considered `up` when an HTTP response is received, even if the response is a 4xx or 5xx status code. Timeouts, DNS failures, and connection failures are considered `down`.
