import asyncio
from typing import List

import grpc
from google.protobuf.json_format import MessageToDict
from pydantic import BaseModel

import protos.windows_service_pb2 as pb2
import protos.windows_service_pb2_grpc as pb2_grpc

# python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. windows_service.proto


class WindowsServiceResponse(BaseModel):
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
    details_request_datetime: str = None


class GWindowsService(object):
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port)
        )

        # bind the client and the server
        self.stub = pb2_grpc.ServiceStub(self.channel)

    async def get_list_of_services(
        self, computer: str, service_name: str = None
    ) -> List[WindowsServiceResponse]:
        """
        Client function to call the rpc for GetServerResponse
        """
        response = []

        async with grpc.aio.insecure_channel(
            '{}:{}'.format(self.host, self.server_port)
        ) as channel:
            stub = pb2_grpc.ServiceStub(channel)

            message_res = pb2.ServiceInfoRequest()
            message_res.request.name = (
                service_name if service_name is not None else ''
            )
            message_res.request.computer = computer

            async for service in stub.get_info(message_res):
                service_dict = MessageToDict(service)
                win = WindowsServiceResponse(**service_dict)
                response.append(win)

            # services = await stub.get_info(message_res)

            # for service in services:
            #     service_dict = MessageToDict(service)
            #     win = WindowsServiceResponse(**service_dict)
            #     response.append(win)

        return response


# if __name__ == '__main__':
#     client = GWindowsService()
#     result = client.get_list_of_services(
#         service_name='SKF @ptitude Transaction Server',
#         computer='BRSAO5CD9466B3H',
#     )
#     print(f'{result}')
