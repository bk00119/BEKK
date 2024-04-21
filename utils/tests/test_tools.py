import utils.tools as tools


def test_get_access_logs():
    # LOG_FILE
    logs = tools.get_access_logs()
    assert len(logs) >= 0
    # ADMIND_LOG_FILE
    admin_logs = tools.get_access_logs(True)
    assert len(admin_logs) >= 0
