# data_manager.py - load/save room data from json file

import json
import os
from models import Classroom, MeetingRoom

class DataManager:
    """Handles reading and writing room data to json file"""

    def __init__(self, file_path=None):
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = "data/classroom_data.json"
        self.rooms = []
        self.load()

    def ensure_directory(self):
        """make sure the data folder exists"""
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print("Created directory: " + folder)
            except OSError as e:
                print("Error creating dir: " + str(e))

    def create_default_data(self):
        """create some default rooms if no data file"""
        self.rooms = [
            Classroom("101", 50),
            Classroom("102", 30),
            MeetingRoom("M01", 10),
        ]
        self.save()

    def load(self):
        """load rooms from json, create default if file missing"""
        if not os.path.exists(self.file_path):
            self.create_default_data()
            return

        try:
            f = open(self.file_path, 'r', encoding='utf-8')
            data = json.load(f)
            f.close()

            self.rooms = []
            for item in data.get("rooms", []):
                rtype = item.get("type", "Classroom")
                bookings = item.get("bookings", {})
                cap = item.get("capacity", 0)

                if rtype == "Meeting Room":
                    room = MeetingRoom(item["id"], cap, bookings)
                else:
                    room = Classroom(item["id"], cap, bookings)
                self.rooms.append(room)

        except (json.JSONDecodeError, KeyError) as e:
            print("Failed to load data: " + str(e))
            self.rooms = []

    def save(self):
        """save all rooms to json"""
        self.ensure_directory()
        room_list = []
        for r in self.rooms:
            room_list.append(r.to_dict())
        data = {"rooms": room_list}
        f = open(self.file_path, 'w', encoding='utf-8')
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()

    def find_room(self, room_id):
        """find room by id, return None if not found"""
        for r in self.rooms:
            if r.id == room_id:
                return r
        return None

    def add_room(self, room):
        """add a new room, return (success, message)"""
        if self.find_room(room.id):
            return False, "Room ID already exists"
        self.rooms.append(room)
        self.save()
        return True, "Room added successfully"

    def remove_room(self, room_id):
        """remove room by id"""
        room = self.find_room(room_id)
        if room:
            self.rooms.remove(room)
            self.save()
            return True, "Room removed successfully"
        return False, "Room not found"
