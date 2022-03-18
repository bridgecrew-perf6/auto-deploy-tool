import logging
import time
from typing import Any
from wmi import WMI, _wmi_object, _wmi_namespace
from .messages import Messages


class WSM:

    WAIT_RESTART_INTERVAL_SEC = 10

    def __init__(
        self,
        service_name: str,
        display_name: str = None,
        description: str = None,
        state: str = None,
        exec_path: str = None,
        computer: str = None,
    ) -> None:
        self.logger = logging.getLogger(__name__)

        self.service_name: str = service_name
        self.display_name: str = display_name if display_name is not None else self.service_name
        self.description: str = description if description is not None else f"service - {self.service_name}"
        self.state: str = state
        self.exec_path: str = exec_path
        self.accept_pause: bool = False
        self.accept_stop: bool = True

        self.process_id: int = 0
        self.start_mode: str = None
        self.status: str = None

        self.computer: str = computer
        self.conn = self.__connect()
        self.service_object = self.__get_service_object()

    def __connect(self) -> _wmi_namespace:
        """Connect to local or remote computer

        Raises:
            err

        Returns:
            WMI Connection: The connection
        """

        if self.computer is None:
            try:
                self.conn = WMI()
                self.logger.debug(f"connected to local computer")
            except Exception as err:
                self.logger.error("error to connect to local computer!!")
                raise err

        try:
            self.conn = WMI(computer=self.computer)
            self.logger.debug(f"connected to remote computer: {self.computer}")
        except Exception as err:
            self.logger.error(f"error to connect to the remote computer: {self.computer}!!")
            raise err

        return self.conn

    def __get_service_object(self) -> _wmi_object:
        """Get the object that represents the windows service

        Returns:
            _wmi_object: WMI Object containing methods and properties
        """

        return self.conn.Win32_Service(Name=self.service_name)[0]

    def __refresh_service_object(self) -> None:
        """Refresh the object info"""
        self.service_object = self.__get_service_object()

    def get_state(self) -> str:
        """Get the state of the service

        Returns:
            The state
        """

        self.__refresh_service_object()
        self.state = self.service_object.State
        return self.state

    def start(self) -> None:
        """Start the service

        Raises:
            Exception: Request was not accepted
            Exception: Service is not running even after request
            err: Error to start the service
        """

        try:
            if self.service_object.State.lower() == "stopped":
                result = self.service_object.StartService()

                if result[0] > 0:
                    raise Exception(f"the request was not accepted. Message: {Messages.response_to_text(result)}")

                self.logger.debug(f"after start: {self.get_state()}")
                if self.get_state().lower() != "running":
                    raise Exception(f"the service is not running even after request. Current State: {self.get_state()}")
            else:
                self.logger.debug("the service is already started.")
        except Exception as err:
            self.logger.error(f"error to start the service {self.service_name}. Current State: {self.get_state()}")
            raise err
        finally:
            self.__refresh_service_object()

    def stop(self) -> None:
        """Stop the service

        Raises:
            Exception: Request was not accepted
            Exception: Service is not stopped even after request
            e: Error to stop the service
        """

        try:
            if self.service_object.State.lower() != "stopped" and self.service_object.AcceptStop:
                result = self.service_object.StopService()

                if result[0] > 0:
                    raise Exception(f"the request was not accepted. Message: {Messages.response_to_text(result)}")

                if self.get_state().lower() != "stopped":
                    raise Exception(f"the service is not stopped even after request. Current State: {self.get_state()}")
        except Exception as err:
            self.logger.error(f"error to stop the service {self.service_name} . Current State: {self.get_state()}")
            raise err
        finally:
            self.__refresh_service_object()

    def restart(self) -> None:
        """restart the service waiting the specific interval"""

        self.stop()
        self.logger.debug(f"waiting {self.WAIT_RESTART_INTERVAL_SEC} seconds to start the service again...")
        time.sleep(self.WAIT_RESTART_INTERVAL_SEC)
        self.start()

    def create(self) -> None:
        """TBD"""
        pass

    def remove(self) -> None:
        """TBD"""
        pass

    def __repr__(self) -> str:
        self.__refresh_service_object()
        return f"({self.service_name}, {self.service_object.State}, {self.service_object.Caption}, {self.service_object.Description}, {self.service_object.State}, {self.exec_path}, {self.service_object.ProcessId})"
