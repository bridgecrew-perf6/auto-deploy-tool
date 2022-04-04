from src.repositories import WindowsService


class TestWindowsService(object):

    WINDOWS_SERVICE_FIXED = "EventLog"

    def test_local_connection_with_service_name(self):
        windows_service = WindowsService(self.WINDOWS_SERVICE_FIXED)
        assert windows_service.conn is not None, "Unable to connect to local host"

    def test_local_connection_with_empty_service_name(self):
        windows_service = WindowsService("")
        assert windows_service.conn is not None, "Unable to connect to local host"

    def test_local_connection_without_service_name(self):
        windows_service = WindowsService()
        assert windows_service.conn is not None, "Unable to connect to local host"

    def test_remote_connection_with_service_name(self):
        windows_service = WindowsService(self.WINDOWS_SERVICE_FIXED, "127.0.0.1")
        assert windows_service.conn is not None, "Unable to connect to local host"

    def test_remote_connection_without_service_name(self):
        windows_service = WindowsService("", "127.0.0.1")
        assert windows_service.conn is not None, "Unable to connect to local host"

    def test_get_state(self):
        windows_service = WindowsService(self.WINDOWS_SERVICE_FIXED)
        state = windows_service.get_state()

        assert state is not None, "Service state is none"
