import config
from database_setup import setup_database
from database_operations import add_monitor, get_monitor, delete_monitor, save_check, get_check_history

def test_add_and_delete_monitor(tmp_path):
    config.database_path = tmp_path / "test_monitor.db"
    setup_database()
    add = add_monitor("https://example.com")
    url_id = add["id"]
    assert get_monitor(url_id) is not None
    delete_monitor(url_id)
    assert get_monitor(url_id) is None

def test_check_history_is_deleted_with_monitor(tmp_path):
    config.database_path = tmp_path / "test_monitor.db"
    setup_database()
    add = add_monitor("https://example.com")
    result = {"status_code": 200, "response_time": 0.42, "up": True, "error": None}
    save_check(add["id"], result)
    assert get_check_history(add['id']) 
    delete_monitor(add['id'])
    assert get_check_history(add['id']) == []