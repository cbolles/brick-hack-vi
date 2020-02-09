from enum import Enum
import json
import time


class WasherStatus(Enum):
    RUNNING = 1
    WAITING_FOR_USER = 2
    AVAILABLE = 3


class Washer:
    def __init__(self, washer_id, mqtt_client):
        self.washer_status = WasherStatus.AVAILABLE
        self.washer_id = washer_id
        self.mqtt_client = mqtt_client
        self.timeout = -1

    def run_cycle(self, cycle_info):
        topic = 'washer/' + str(self.washer_id) + '/run_cycle'
        self.mqtt_client.publish(topic, json.dumps(cycle_info))
        self.washer_status = WasherStatus.RUNNING

    def cycle_complete(self):
        self.washer_status = WasherStatus.WAITING_FOR_USER
        self.timeout = time.time() + 30

    def unlock(self):
        topic = 'washer/' + str(self.washer_id) + '/unlock'
        self.mqtt_client.publish(topic, '')
        self.washer_status = WasherStatus.AVAILABLE


class WasherDatabase:
    def __init__(self, mqtt_client):
        self.washers = [Washer(id, mqtt_client) for id in range(1, 3)]

    def get_available_washers(self):
        return [washer for washer in self.washers if washer.washer_status == WasherStatus.AVAILABLE]

    def get_by_id(self, washer_id):
        for washer in self.washers:
            if washer.washer_id == washer_id:
                return washer

    def check_timeouts(self):
        waiting_washers = [washer for washer in self.washers if washer.washer_status == WasherStatus.WAITING_FOR_USER]
        current_time = time.time()
        [washer.unlock() for washer in waiting_washers if current_time >= washer.timeout]
