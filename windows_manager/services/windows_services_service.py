import protos.windows_service_pb2 as pb2
import protos.windows_service_pb2_grpc as pb2_grpc
from windows_services_service import WindowsServiceService


class Service(pb2_grpc.ServiceServicer):
    def get_info(self, request, context):

        basicRequest = request.request

        service_name = basicRequest.name if basicRequest.name else None
        computer = basicRequest.computer

        win_service = WindowsServiceService(
            service_name=service_name, computer_name=computer
        )

        services_info = []

        if service_name is None:
            services_info = win_service.get_all_objects()
        else:
            services_info.append(win_service.get_info())

        for service in services_info:
            yield pb2.ServiceResponse(**service.dict())
