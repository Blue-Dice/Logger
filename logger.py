import sys
import logging
import coloredlogs
from decouple import config

INFO = logging.INFO
DEBUG = logging.DEBUG
REPORT = INFO + 5
SUCCESS = INFO + 6
CRITICAL = logging.CRITICAL

logging.addLevelName(REPORT, 'REPORT')
logging.addLevelName(SUCCESS, 'SUCCESS')

class SchedulerLogger(logging.Logger):

    def __init__(self, name, console_level):
        super().__init__(name, console_level)
        self._stream_handler()
        if config('CREATE_RECORD_LOG', cast=bool, default=False):
            self._file_handler()
    
    def _stream_handler(self):
        self.streamHandler = logging.StreamHandler(sys.stdout)
        self.streamHandler.setFormatter(self._build_stream_formatter())
        super().addHandler(self.streamHandler)
    
    def _file_handler(self):
        self.fileHandler = logging.FileHandler(filename='records.log')
        self.fileHandler.setFormatter(self._build_file_formatter())
        super().addHandler(self.fileHandler)
    
    def _build_file_formatter(self):
        return logging.Formatter(
            'DateTime:[%(asctime)s] -> Message:[%(message)s]', 
            '%m/%d/%Y - %H:%M:%S'
        )

    def _build_stream_formatter(self):
        return coloredlogs.ColoredFormatter(
            'DateTime: [%(asctime)s] -> Message:[%(message)s]',
            '%m/%d/%Y - %H:%M:%S',
            level_styles = {
                'debug': {'color': 'yellow', 'bold': True},
                'report': {'bold': True},
                'success': {'bold': True, 'color': 'green'},
                'critical': {'bold': True, 'color': 'red'},
            }
        )

    def log(self, msg, level=INFO):
        super().log(level, msg)
        
logger = SchedulerLogger('Scheduler', DEBUG)

def debug(msg):
    msg = f'#DEBUG -> {msg}'
    return logger.log(msg, level=DEBUG)

def report(msg):
    msg = f'#REPORT -> {msg}'
    return logger.log(msg, level=REPORT)

def success(msg):
    msg = f'#SUCCESS -> {msg}'
    return logger.log(msg, level=SUCCESS)

def failure(msg):
    msg = f'#FAILURE -> {msg}'
    return logger.log(msg, level=CRITICAL)
