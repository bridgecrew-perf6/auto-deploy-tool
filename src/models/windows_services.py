from datetime import datetime


class WindowsServices:
    def __init__(
        self,
        name: str = None,
        description: str = None,
        accept_pause: str = None,
        accept_stop: str = None,
        caption: str = None,
        check_point: str = None,
        creation_classname: str = None,
        delayed_auto_start: str = None,
        desktop_interact: str = None,
        display_name: str = None,
        error_control: str = None,
        exit_code: str = None,
        path_name: str = None,
        process_id: str = None,
        service_specific_exit_code: str = None,
        service_type: str = None,
        started: str = None,
        start_mode: str = None,
        start_name: str = None,
        state: str = None,
        status: str = None,
        system_creation_classname: str = None,
        system_name: str = None,
        tag_id: str = None,
        wait_hint: str = None,
    ) -> None:
        self.name = name
        self.description = description
        self.accept_pause = accept_pause
        self.accept_stop = accept_stop
        self.caption = caption
        self.check_point = check_point
        self.creation_classname = creation_classname
        self.delayed_auto_start = delayed_auto_start
        self.desktop_interact = desktop_interact
        self.display_name = display_name
        self.error_control = error_control
        self.exit_code = exit_code
        self.path_name = path_name
        self.process_id = process_id
        self.service_specific_exit_code = service_specific_exit_code
        self.service_type = service_type
        self.started = started
        self.start_mode = start_mode
        self.start_name = start_name
        self.state = state
        self.status = status
        self.system_creation_classname = system_creation_classname
        self.system_name = system_name
        self.tag_id = tag_id
        self.wait_hint = wait_hint
        self.details_request_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
