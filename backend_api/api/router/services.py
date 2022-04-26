from typing import List, Optional
import logging

from fastapi import APIRouter, HTTPException, status

from grpc_windows_service import GWindowsService, WindowsServiceResponse
from responses import IResponseBaseJson

services_routes = APIRouter()


@services_routes.get('/',
description="Retrieve service information from an specific service name and an specific computer",
response_model=IResponseBaseJson[WindowsServiceResponse])
async def get_service_info(computer: str, service: str):

    try:
        client = GWindowsService()
        services = await client.get_list_of_services(
            computer=computer, service_name=service
        )
    except Exception as err:
        logging.exception(f"error to retrieve the service ({service}) info from {computer}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not services:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="service not found")

    return IResponseBaseJson[WindowsServiceResponse](
        status=status.HTTP_200_OK,
        message=f"show '{service}' information from {computer}",
        data=services[0],
    )


@services_routes.get('/list', 
description="Retrieve service information from all services in an specific computer",
response_model=IResponseBaseJson[List[WindowsServiceResponse]])
async def list_all_services(computer: str):

    try:
        client = GWindowsService()
        services = await client.get_list_of_services(computer=computer)
    except:
        logging.exception(f"error to retrieve the list of services from {computer}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not services:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="services not found")

    return IResponseBaseJson[List[WindowsServiceResponse]](
        status=status.HTTP_200_OK,
        message=f'list all services from {computer}',
        data=services,
    )
