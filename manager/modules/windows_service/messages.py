VALUE_INT = {
    0: "The request was accepted.",
    1: "The request is not supported.",
    2: "The user did not have the necessary access.",
    3: "The service cannot be stopped because other services that are running are dependent on it.",
    4: "The requested control code is not valid, or it is unacceptable to the service.",
    5: "The requested control code cannot be sent to the service because the state of the service (Win32_BaseService.State property) is equal to 0, 1, or 2.",
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
    22: "The account which this service is to run under is either invalid or lacks the permissions to run the service.",
    23: "The service exists in the database of services available from the system.",
    24: "The service is currently paused in the system.",
}


class Messages:
    def __init__(self) -> None:
        pass

    @staticmethod
    def response_to_text(response: tuple) -> str:
        """convert service response to his equivalent readable text message

        Args:
            response (tuple): the service response provided by the WMI

        Raises:
            ValueError

        Returns:
            str: text readable message
        """

        return Messages.response_number_to_text(response[0])

    @staticmethod
    def response_number_to_text(value: int) -> str:
        """return the text message for the int value

        Args:
            value_int (int): error int value

        Returns:
            str: text message
        """
        try:
            return VALUE_INT[value]
        except:
            return f"unkown response for value: {value}"

    def get_known_messages(self) -> dict:
        return VALUE_INT
