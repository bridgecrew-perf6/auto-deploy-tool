import logging
import subprocess
from typing import Tuple

from wmi import WMI, _wmi_namespace, _wmi_object

from src.models import WindowsServices


class WindowsService:
    def __init__(self, service_name: str = None, computer_name: str = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.service_name = service_name
        self.computer_name = computer_name

        self.logger.debug(f"WINDOWS SERVICE: {self.service_name}. COMPUTER NAME: {computer_name}")

        self.conn = self.__connect_wmi()
        self.object = self.__get_service_object()
        self.windows_service: WindowsServices = self.__windows_service_data()

    def create(self, display_name: str, path_name: str, start_mode: str = "auto") -> None:
        """
        Create a windows service

        Args:
            display_name (str): The name that will be displayed in the service list
            path_name (str): the bin path with the additional parameters
            start_mode (str, optional): start mode . Defaults to "auto".

        Raises:
            NoServiceNameDefined: no service named defined
            UnableToStart: unable to start the service
            Exception: sc.exe message error
            err: error to create the service
        """

        if self.service_name is None:
            raise NoServiceNameDefined("you must provide the service name you want to create")

        try:
            command = [
                "sc.exe",
                "create",
                f"{self.service_name}",
                f'binPath= "{path_name}"',
                f"DisplayName= {display_name}",
                f"start={start_mode}",
            ]

            if self.computer_name is not None:
                command.insert(1, self.computer_name)
                self.logger.debug(
                    f"the service will be created on the remote server: {self.computer_name}"
                )

            process = subprocess.run(args=command, stdout=subprocess.PIPE, universal_newlines=True)

            self.logger.debug(process)

            response = self.__readable_subprocess_return(process)
            self.logger.debug(response[1])

            if not response[0]:
                raise Exception(response[1])

            if self.start()[0]:
                raise UnableToStart

        except Exception as err:
            raise err

    def delete(self) -> None:
        """
        delete the service

        Raises:
            NoServiceNameDefined: no service name defined
            UnableToStop: unable to stop the service
            Exception: sc.exe message error
            err: error to delete
        """

        if self.service_name is None:
            raise NoServiceNameDefined("you must provide the service name you want to delete")

        try:
            if not self.stop()[0]:
                raise UnableToStop

            command = ["sc.exe", "delete", self.service_name]

            if self.computer_name is not None:
                command.insert(1, self.computer_name)
                self.logger.debug(
                    f"the service will be created on the remote server: {self.computer_name}"
                )

            process = subprocess.run(args=command, stdout=subprocess.PIPE, universal_newlines=True)

            response = self.__readable_subprocess_return(process)
            self.logger.debug(response[1])

            if not response[0]:
                raise Exception(response[1])

        except Exception as err:
            raise err

    def restart(self) -> Tuple[bool, str]:
        """
        Restart the windows service

        Raises:
            UnknownState: unable to get the service state
            permission_err: user has no permission to perform the action
            unable_start_err: unable to start the service
            unable_stop_err: unable to stop the service

        Returns:
            Tuple[bool, str]: is running or not, service state
        """

        try:
            if self.is_running() and self.windows_service.accept_stop:
                _ = self.stop()

            if self.is_stopped():
                _ = self.start()

            if not self.is_running() and not self.is_stopped():
                raise UnknownState("the service is not ruuning and not stopped")

        except NoPermission as permission_err:
            raise permission_err
        except UnableToStart as unable_start_err:
            raise unable_start_err
        except UnableToStop as unable_stop_err:
            raise unable_stop_err
        finally:
            self.__refresh_windows_service()

        return [self.is_running(), self.windows_service.state]

    def stop(self) -> Tuple[bool, str]:
        """
        Stops the service

        Raises:
            NoPermission: User has not permission to perform the action
            NotRunning: Error to stop
            err: Exception

        Returns:
            Tuple[bool, str]: Is stopped or Not, Current state
        """

        try:
            if self.is_running() and self.windows_service.accept_stop:
                self.logger.debug("starting service")
                result = self.object.StopService()

                if result[0] > 0:
                    if result[0] == 2:
                        raise NoPermission(Messages.get_readable_message(result[0]))
                    else:
                        raise Exception(Messages.get_readable_message(result[0]))

                if not self.is_stopped():
                    raise UnableToStop("Service is not stopped even after try to stop.")

                self.logger.debug("service has been stopped")
        except Exception as err:
            raise err
        finally:
            self.__refresh_windows_service()

        return [self.is_running(), self.windows_service.state]

    def start(self) -> Tuple[bool, str]:
        """
        Start the service

        Raises:
            NoPermission: User has not permission to perform the action
            NotRunning: Error to start
            err: Exception

        Returns:
            Tuple[bool, str]: Is running or Not, Current state
        """

        try:
            if not self.is_running():
                self.logger.debug("starting service")
                result = self.object.StartService()

                if result[0] > 0:
                    if result[0] == 2:
                        raise NoPermission(Messages.get_readable_message(result[0]))
                    else:
                        raise Exception(Messages.get_readable_message(result[0]))

                if self.is_running():
                    raise UnableToStart("Service is not running even after try to start.")

                self.logger.debug("service has been started")

        except Exception as err:
            raise err
        finally:
            self.__refresh_windows_service()

        return [self.is_running(), self.windows_service.state]

    def is_stopped(self) -> bool:
        """
        Check if the service is stopped

        Returns:
            bool: Stopped or Not
        """

        self.__refresh_windows_service()
        return self.windows_service.state.lower() == "stopped"

    def is_running(self) -> bool:
        """
        Check if the service is running

        Returns:
            bool: Running or Not Running
        """

        self.__refresh_windows_service()
        return self.windows_service.state.lower() == "running"

    def get_info(self) -> WindowsServices:
        """
        Get the service information

        Returns:
            WindowsServices: Object containing the information
        """

        self.__refresh_windows_service()
        return self.windows_service

    def get_state(self) -> str:
        """
        Get the current windows service state

        Returns:
            str: The service state
        """
        self.__refresh_windows_service()
        return self.windows_service.state

    def __readable_subprocess_return(
        self, completed_process: subprocess.CompletedProcess
    ) -> Tuple[bool, str, int]:

        return_status = False
        return_msg = completed_process.stdout
        return_code = completed_process.returncode

        if return_code == 0:
            return_status = True

        return [return_status, return_msg, return_code]

    def __refresh_windows_service(self) -> None:
        """
        refresh the windows service object
        """
        self.logger.debug("refreshing data from windows service")
        self.__get_service_object()
        self.windows_service = self.__windows_service_data()

    def __connect_wmi(self) -> _wmi_namespace:
        """
        Connect to WMI interface

        Raises:
            err: Exception
            err: Exception

        Returns:
            _wmi_namespace: connection object
        """

        if self.computer_name is None:
            try:
                conn = WMI()
                self.logger.debug("connected to service on local machine")
            except Exception as err:
                self.logger.exception("unable to connect to service on local machine")
                raise err
        else:
            try:
                conn = WMI(computer=self.computer_name)
                self.logger.debug(f"connected to service on remote machine: {self.computer_name}")
            except Exception as err:
                self.logger.exception(
                    f"unable to connect to service on remote machine: {self.computer_name}"
                )
                raise err

        return conn

    def __get_service_object(self) -> _wmi_object:
        """
        Get the windows service object

        Raises:
            NoServiceNameDefined
            err: raise exception

        Returns:
            _wmi_object: windows service object
        """
        try:
            self.logger.debug("getting service object for the service")
            return self.conn.Win32_Service(Name=self.service_name)[0]
        except IndexError:
            self.logger.info(f"{self.service_name} does not exists")
            return None
        except Exception as err:
            raise err

    def __windows_service_data(self) -> WindowsServices:
        """
        Get the windows service informations

        Returns:
            WindowsServices: Object contaning the data
        """
        if self.object is None:
            return WindowsServices(name=self.service_name)

        service_object = self.object
        windows_service = WindowsServices(
            name=service_object.Name,
            description=service_object.Description,
            accept_pause=service_object.AcceptPause,
            accept_stop=service_object.AcceptStop,
            caption=service_object.Caption,
            check_point=service_object.CheckPoint,
            creation_classname=service_object.CreationClassName,
            delayed_auto_start=service_object.DelayedAutoStart,
            desktop_interact=service_object.DesktopInteract,
            display_name=service_object.DisplayName,
            error_control=service_object.ErrorControl,
            exit_code=service_object.ExitCode,
            path_name=service_object.PathName,
            process_id=service_object.ProcessId,
            service_specific_exit_code=service_object.ServiceSpecificExitCode,
            service_type=service_object.ServiceType,
            started=service_object.Started,
            start_mode=service_object.StartMode,
            start_name=service_object.StartName,
            state=service_object.State,
            status=service_object.Status,
            system_creation_classname=service_object.SystemCreationClassName,
            system_name=service_object.SystemName,
            tag_id=service_object.TagId,
            wait_hint=service_object.WaitHint,
        )

        return windows_service

    def __repr__(self) -> str:
        self.__refresh_windows_service()
        return (
            f" <Name: {self.windows_service.name}, "
            f"Description: {self.windows_service.description}, "
            f"Caption: {self.windows_service.caption}, "
            f"State: {self.windows_service.state}, "
            f"Path: {self.windows_service.path_name}, "
            f"ProcessId: {self.windows_service.process_id}>"
        )


class NoPermission(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class UnableToStart(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class UnableToStop(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class UnknownState(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class NoServiceNameDefined(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)


class Messages:

    VALUE_INT = {
        0: "The request was accepted.",
        1: "The request is not supported.",
        2: "The user did not have the necessary access.",
        3: "The service cannot be stopped because other services that are running are dependent on it.",
        4: "The requested control code is not valid, or it is unacceptable to the service.",
        5: """The requested control code cannot be sent to the service because the state of the service
     (Win32_BaseService.State property) is equal to 0, 1, or 2""",
        6: "The service has not been started.",
        7: "The service did not respond to the start request in a timely fashion.",
        8: "An unknown failure occurred when starting the service.",
        9: "The directory path to the service executable file was not found.",
        10: "The service is already running.",
        11: "The database to add a new service is locked.",
        12: "A dependency for which this service relies on has been removed from the system.",
        13: "The service failed to find the service needed from a dependent service.",
        14: "The service has been disabled from the system.",
        15: "The service does not have the correct authentication to run on the system.",
        16: "This service is being removed from the system.",
        17: "There is no execution thread for the service.",
        18: "There are circular dependencies when starting the service.",
        19: "There is a service running under the same name.",
        20: "There are invalid characters in the name of the service.",
        21: "Invalid parameters have been passed to the service.",
        22: "The account which this service is to run under is either invalid or lacks the permissions \
            to run the service.",
        23: "The service exists in the database of services available from the system.",
        24: "The service is currently paused in the system.",
    }

    @staticmethod
    def get_readable_message(message_number: int):
        return Messages.VALUE_INT[message_number]
