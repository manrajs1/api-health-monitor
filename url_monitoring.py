import httpx
import time
from urllib.parse import urlsplit
import ipaddress
import socket

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
        return {"status_code": None, "response_time": time_taken, "up": False, "error":"Request Error"}
    
    
def validate_url(url):
    url_split = urlsplit(url)
    # Getting scheme of the url to check if it is http or https
    url_scheme = url_split.scheme
    if url_scheme != "http" and url_scheme != "https":
        return False
    url_hostname = url_split.hostname
    if url_hostname is None:
        return False
    # Getting the hostname full info including ip and checking if website is unsafe
    try:
        url_info = socket.getaddrinfo(url_hostname, None)
    except socket.gaierror:
        return False
    for row in url_info:
        ip_address = row[4][0]
        ip_address = ipaddress.ip_address(ip_address)
        if ip_address.is_private:
            return False
        elif ip_address.is_loopback:    
            return False
        elif ip_address.is_link_local:    
            return False
        elif ip_address.is_reserved:    
            return False
        elif ip_address.is_unspecified:    
            return False
        elif ip_address.is_multicast:
            return False
    return True