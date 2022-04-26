import logging
from concurrent import futures

import grpc
import protos.windows_service_pb2_grpc as pb2_grpc
from windows_services_service import Service


async def start():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ServiceServicer_to_server(Service(), server)

    server.add_insecure_port('[::]:50051')
    logging.info('starting gRPC server. Running on [::]:50051')

    await server.start()
    await server.wait_for_termination()
