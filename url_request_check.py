import httpx
import time

def request_check(url):
    try:
        start = time.perf_counter()
        response = httpx.get(url, timeout=5.0)
        end = time.perf_counter()
        time_taken = end - start
        time_taken = round(time_taken, 2)
        status = {"status_code": response.status_code, "response_time": time_taken, "up": True, "error": None}
        return status
    except httpx.RequestError:
        end = time.perf_counter()
        time_taken = end - start
        time_taken = round(time_taken, 2)
        return {"status_code": None, "response_time": time_taken, "up": False, "errror":"Request Error"}