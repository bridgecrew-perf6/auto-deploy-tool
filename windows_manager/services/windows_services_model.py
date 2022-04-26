from datetime import datetime

from pydantic import BaseModel


class RestartIn(BaseModel):
    computer: str
    name: str


class StopIn(BaseModel):
    computer: str
    name: str


class StartIn(BaseModel):
    computer: str
    name: str


class WindowsServicesOut(BaseModel):
    computer: str = None
    name: str = None
    description: str = None
    accept_pause: bool = False
    accept_stop: bool = False
    caption: str = None
    check_point: int = 0
    creation_classname: str = None
    delayed_auto_start: str = None
    desktop_interact: str = None
    display_name: str = None
    error_control: str = None
    exit_code: int = 0
    path_name: str = None
    process_id: int = 0
    service_specific_exit_code: int = 0
    service_type: str = None
    started: bool = False
    start_mode: str = None
    state: str = None
    status: str = None
    system_creation_classname: str = None
    system_name: str = None
    start_name: str = None
    tag_id: int = 0
    wait_hint: int = 0
    details_request_datetime: str = datetime.now().strftime('%d/%m/%Y %H:%M')
