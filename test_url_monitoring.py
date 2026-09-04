from url_monitoring import validate_url


def test_public_https_url_is_allowed():
    assert validate_url("https://example.com") is True
    assert validate_url("https://manrajsingh.dev/") is True
    assert validate_url("http://httpforever.com/") is True
    
def test_loopback_url_is_blocaked():
    assert validate_url("http://127.0.0.1:8080/") is False
    assert validate_url("http://localhost:3000/") is False

def test_private_ip_is_blocked():
    assert validate_url("http://10.1.2.3") is False
    assert validate_url("http://172.18.55.23") is False
    assert validate_url("http://192.168.0.0") is False
    
def test_non_http_scheme_is_blocked():
    assert validate_url("ftp://example.com") is False

    
def test_missing_scheme_is_blocked():
    assert validate_url("manrajsingh.dev/") is False
    assert validate_url("httpforever.com/") is False
    
def test_unresolvable_hostname_is_blocked():
    assert validate_url("https://this-domain-should-not-exist.invalid") is False
    
