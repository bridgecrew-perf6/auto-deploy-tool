import logging
from logging.handlers import TimedRotatingFileHandler
from src.repositories import WindowsService
from time import sleep

log_handler = TimedRotatingFileHandler("app.log", when="w0", backupCount=5)
logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(name)s %(module)s-%(lineno)04d %(levelname)8s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
    handlers=[log_handler],
)

w = WindowsService("SKFDatadogConsumerDemo01")
w.stop()

w.start()
sleep(3)
w.stop()
w.stop()

w.restart()
