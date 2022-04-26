import logging
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from router.services import services_routes

log_handler_rotation_file = TimedRotatingFileHandler(
    filename='api.log', when='w0', backupCount=4
)
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(name)s %(module)s-%(lineno)04d %(levelname)8s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
    handlers=[log_handler_rotation_file],
)



app = FastAPI(default_response_class=JSONResponse)
app.include_router(prefix='/services', router=services_routes)


@app.get('/')
def welcome(request: Request):
    return {
        'message': 'Welcome to autodeploy API. Give a try into our documentations',
        'documentation': [
            f'{request.url._url}docs',
            f'{request.url._url}redoc',
        ],
    }


# @app.get('/', response_model=IResponseBaseJson[List[Usuario]])
# async def welcome():

#     item = [Usuario(id=45,nome="",email="")]

#     if item is not None:
#          raise HTTPException(status_code=404, detail=item)

#     return IResponseBaseJson[List[Usuario]](status=200, message="working fine", data=item)
