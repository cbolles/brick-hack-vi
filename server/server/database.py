from enum import Enum


class WasherStatus(Enum):
    RUNNING = 1
    WAITING_FOR_USER = 2
    AVAILABLE = 3


class Washer:
    def __init__(self, washer_id):
        self.washer_status = WasherStatus.AVAILABLE
        self.washer_id = washer_id


class WasherDatabase:
    def __init__(self):
        self.washers = [Washer(id) for id in range(1, 11)]

    def get_available_washers(self):
        return [washer for washer in self.washers if washer.washer_status == WasherStatus.AVAILABLE]

    def get_by_id(self, washer_id):
        for washer in self.washers:
            if washer.washer_id == washer_id:
                return washer

    def set_washer_running(self, washer_id):
        self.get_by_id(washer_id).washer_status = WasherStatus.RUNNING

    def set_washer_available(self, washer_id):
        self.get_by_id(washer_id).washer_status = WasherStatus.AVAILABLE
