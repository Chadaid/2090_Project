# models.py - room classes (OOP: Inheritance, Polymorphism)


class Room:
    """Base class for rooms"""

    def __init__(self, room_id, capacity, bookings=None):
        self.id = room_id
        self.capacity = int(capacity)
        if bookings:
            self.bookings = bookings
        else:
            self.bookings = {}

    def room_type(self):
        return "Room"

    def get_info(self):
        count = len(self.bookings)
        return "[Room] ID: " + self.id + " | Capacity: " + str(self.capacity) + " | Bookings: " + str(count)

    def is_available(self, time_slot):
        return time_slot not in self.bookings

    def book(self, time_slot, user_name):
        """try to book a time slot, return (success, message)"""
        if not self.is_available(time_slot):
            return False, "Already booked by " + self.bookings[time_slot]
        self.bookings[time_slot] = user_name
        return True, "Booking successful"

    def cancel_booking(self, time_slot):
        if time_slot in self.bookings:
            del self.bookings[time_slot]
            return True, "Cancelled successfully"
        return False, "No booking found for this time slot"

    def to_dict(self):
        """convert to dict for saving to json"""
        return {
            "id": self.id,
            "capacity": self.capacity,
            "type": self.room_type(),
            "bookings": dict(self.bookings)
        }

    def __str__(self):
        return self.room_type() + " " + self.id + " (Capacity: " + str(self.capacity) + ")"


# --- Subclasses ---

class Classroom(Room):
    """Classroom for teaching"""

    def room_type(self):
        return "Classroom"

    def get_info(self):
        count = len(self.bookings)
        return "[Classroom] ID: " + self.id + " | Capacity: " + str(self.capacity) + " seats | Bookings: " + str(count)


class MeetingRoom(Room):
    """Meeting room for meetings/seminars"""

    def room_type(self):
        return "Meeting Room"

    def get_info(self):
        count = len(self.bookings)
        return "[Meeting Room] ID: " + self.id + " | Capacity: " + str(self.capacity) + " people | Bookings: " + str(count)
