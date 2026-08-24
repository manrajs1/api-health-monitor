import httpx
import time


def request_check(url):
    try:
        start = time.perf_counter()

        request = httpx.get(url, timeout=5.0)

        end = time.perf_counter()

        time_taken = end - start
        time_taken = round(time_taken, 2)
        status = {"status code": request.status_code, "response time": time_taken, "Up": True, "Error": None}
        return status
    except httpx.RequestError:
        end = time.perf_counter()
        time_taken = end - start
        time_taken = round(time_taken, 2)
        return {"status code": None, "response time": time_taken, "Up": False, "Error":"Request Error"}

