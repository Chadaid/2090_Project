# booking_manager.py - booking logic and time slot handling

from data_manager import DataManager
from models import Classroom, MeetingRoom

# weekday and time slot mappings
WEEK_MAP = {
    "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu",
    "5": "Fri", "6": "Sat", "7": "Sun"
}
SLOT_MAP = {
    "1": "Morning", "2": "Afternoon"
}

# reverse maps for GUI dropdowns
WEEK_REVERSE = {}
for k, v in WEEK_MAP.items():
    WEEK_REVERSE[v] = k

SLOT_REVERSE = {}
for k, v in SLOT_MAP.items():
    SLOT_REVERSE[v] = k


def format_time_slot(weekday_num, slot_num):
    """turn number inputs into time string like 'Mon Morning'"""
    week = WEEK_MAP.get(str(weekday_num))
    slot = SLOT_MAP.get(str(slot_num))
    if not week or not slot:
        return None
    return week + " " + slot


def get_all_time_slots():
    """generate all 14 time slots (7 days x 2 slots)"""
    slots = []
    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        for s in ["Morning", "Afternoon"]:
            slots.append(d + " " + s)
    return slots


class BookingManager:
    """Handles booking operations, uses DataManager for data access"""

    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_all_rooms(self):
        return list(self.data_manager.rooms)

    def get_room_schedule(self, room_id):
        """get schedule for a room, returns (room, bookings) or (None, error msg)"""
        room = self.data_manager.find_room(room_id)
        if not room:
            return None, "Room not found"
        return room, dict(room.bookings)

    def book_room(self, room_id, time_slot, user_name):
        """book a room for given time slot"""
        room = self.data_manager.find_room(room_id)
        if not room:
            return False, "Room not found"
        success, msg = room.book(time_slot, user_name)
        if success:
            self.data_manager.save()
        return success, msg

    def cancel_booking(self, room_id, time_slot):
        """cancel booking for a room"""
        room = self.data_manager.find_room(room_id)
        if not room:
            return False, "Room not found"
        success, msg = room.cancel_booking(time_slot)
        if success:
            self.data_manager.save()
        return success, msg

    def add_room(self, room_id, capacity, room_type="Classroom"):
        """create and add a new room"""
        if room_type == "Meeting Room":
            room = MeetingRoom(room_id, capacity)
        else:
            room = Classroom(room_id, capacity)
        return self.data_manager.add_room(room)
