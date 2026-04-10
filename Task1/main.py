# main.py - program entry

from data_manager import DataManager
from booking_manager import BookingManager
from gui import BookingApp

def main():
    # create data manager and booking manager, then start GUI
    data_mgr = DataManager()
    booking_mgr = BookingManager(data_mgr)

    app = BookingApp(booking_mgr)
    app.mainloop()

if __name__ == "__main__":
    main()
