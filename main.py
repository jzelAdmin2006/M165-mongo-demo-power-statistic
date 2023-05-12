import datetime
import os
import time

import psutil
from pymongo import MongoClient


class Power:
    def __init__(self, timestamp=None):
        self.cpu = psutil.cpu_percent()
        self.ram_total = psutil.virtual_memory().total
        self.ram_usage = psutil.virtual_memory().used
        self.timestamp = datetime.datetime.now() if timestamp is None else timestamp


def log_power_usage(db):
    power = Power()
    db.power_usage.insert_one(power.__dict__)
    print("Inserted power usage: " + str(power.__dict__))


def prune_power_usage(db):
    count = db.power_usage.count_documents({})
    if count > 10000:
        cursor = db.power_usage.find().sort("timestamp", 1).limit(count - 10000)
        ids = [x["_id"] for x in cursor]
        db.power_usage.delete_many({"_id": {"$in": ids}})


connection_string = os.environ['MONGODB_CONNECTION_STRING']
client = MongoClient(connection_string)
db = client["power_statistics"]

while True:
    log_power_usage(db)
    prune_power_usage(db)
    time.sleep(1)
