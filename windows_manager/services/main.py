import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler

import server

log_handler_rotation_file = TimedRotatingFileHandler(
    filename='gprc_server.log', when='w0', backupCount=4
)
logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(module)s-%(lineno)04d %(levelname)8s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
    handlers=[log_handler_rotation_file],
)

if __name__ == '__main__':
    asyncio.run(server.start())
