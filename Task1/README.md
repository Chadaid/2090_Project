# Classroom Booking System

A GUI-based classroom booking system built with Python and Tkinter.

## Features
- Browse all rooms (Classroom / Meeting Room)
- View weekly schedule for any room (7 days × 2 slots)
- Book and cancel room reservations
- Admin panel: add or remove rooms
- Data stored in JSON (`data/classroom_data.json`)

## Project Structure
| File | Description |
|------|-------------|
| `main.py` | Entry point |
| `models.py` | Room class hierarchy (`Room` → `Classroom`, `MeetingRoom`) |
| `data_manager.py` | JSON data loading and saving |
| `booking_manager.py` | Booking logic and time slot handling |
| `gui.py` | Tkinter GUI |

## How to Run
```bash
cd Task1
python main.py
```
