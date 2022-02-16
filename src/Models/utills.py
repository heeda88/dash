import datetime 

from logging.config import dictConfig
import logging


class LogStamp():

    def logtime():
        dt_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        ouTime=f"{dt_kst} ( UTC + 09:00 )"
        return ouTime

    def logTurnOn():
        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': f'[{logtime()}] %(levelname)s %(module)s - %(funcName)s: %(message)s',
                }
            },
            'handlers': {
                'file': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': 'debug.log',
                    'formatter': 'default',
                },
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['file']
            }
        })
        logging.debug("logging on")
