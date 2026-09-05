import httpx
import time
from urllib.parse import urlsplit
import ipaddress
import socket

def request_check(url):
    try:
        # Starting the stopwatch
        start = time.perf_counter()
        
        # Sending the HTTP request and getting a Response object
        response = httpx.get(url, timeout=5.0)
        
        # Ending the stopwatch
        end = time.perf_counter()
        
        # Calculating the response time and rounding it to two decimal places
        time_taken = end - start
        time_taken = round(time_taken, 2)
        
        # Storing the status code, response time, and whether the server was reachable
        # up=True means an HTTP response was received, even if it was a 4xx or 5xx response
        status = {"status_code": response.status_code, "response_time": time_taken, "up": True, "error": None}
        return status
    
    # Handling request failures such as DNS errors, timeouts, and connection failures
    except httpx.RequestError:
        end = time.perf_counter()
        time_taken = end - start
        time_taken = round(time_taken, 2)
        # Returning a failed check when no HTTP response was received
        return {"status_code": None, "response_time": time_taken, "up": False, "error":"Request Error"}
    
    
def validate_url(url):
    # Splitting the URL into different parts using urllib.parse 
    url_split = urlsplit(url)
    
    # Getting the URL scheme and allowing only HTTP or HTTPS
    url_scheme = url_split.scheme
    if url_scheme != "http" and url_scheme != "https":
        return False
    
    # Getting the hostname and rejecting the URL if no hostname exists
    url_hostname = url_split.hostname
    if url_hostname is None:
        return False
    
    # Resolving the hostname into network address information
# getaddrinfo() can return multiple rows because one hostname can have multiple IP addresses
    try:
        url_info = socket.getaddrinfo(url_hostname, None)
    # DNS resolution failed, so the hostname could not be resolved
    except socket.gaierror:
        return False
    
    for row in url_info:
        # Each row contains network information like:
        # (family, type, protocol, canonical_name, address)
        # row[4] is the address tuple, for example ("93.184.216.34", 0)
        # row[4][0] gets just the IP address string
        ip_address = row[4][0]
        
        # Converting the IP string into an IP address object
        ip_address = ipaddress.ip_address(ip_address)
        
        # Rejecting IP addresses that should not be accessed by the monitor
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
    
    # All resolved IP addresses passed the safety checks
    return True