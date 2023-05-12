import datetime

import psutil


class Power:
    def __init__(self, timestamp=None):
        self.cpu = psutil.cpu_percent()
        self.ram_total = psutil.virtual_memory().total
        self.ram_usage = psutil.virtual_memory().used
        self.timestamp = datetime.datetime.now() if timestamp is None else timestamp
