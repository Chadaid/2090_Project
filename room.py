import json
import os


class Room:
    def __init__(self, room_id, capacity, bookings=None):
        self.room_id = room_id
        self.capacity = capacity
        self.bookings = bookings if bookings is not None else {}

    def is_available(self, time_slot):
        return time_slot not in self.bookings

    def book(self, time_slot, user_name):
        if not self.is_available(time_slot):
            return False, self.bookings[time_slot] # 已经被预订
        self.bookings[time_slot] = user_name
        return True, ""

    def cancel_booking(self, time_slot):
        if time_slot in self.bookings:
            del self.bookings[time_slot]
            return True
        return False

    def to_dict(self):
        """将对象转换为字典，以便保存为 JSON"""
        return {
            "id": self.room_id,
            "capacity": self.capacity,
            "bookings": self.bookings
        }