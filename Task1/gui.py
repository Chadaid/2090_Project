# gui.py - tkinter GUI for classroom booking system

import tkinter as tk
from tkinter import ttk, messagebox
from booking_manager import BookingManager, WEEK_MAP, SLOT_MAP, format_time_slot


class BookingApp(tk.Tk):
    """Main window of the booking app, inherits tk.Tk"""

    def __init__(self, booking_manager):
        super().__init__()
        self._manager = booking_manager

        self.title("Classroom Booking System")
        self.geometry("750x520")
        self.resizable(False, False)

        self._create_widgets()
        self._refresh_room_list()

    def _create_widgets(self):
        """set up the tabs"""
        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._create_room_list_tab()
        self._create_schedule_tab()
        self._create_booking_tab()
        self._create_cancel_tab()
        self._create_admin_tab()

    # --- Tab 1: Room List ---
    def _create_room_list_tab(self):
        frame = ttk.Frame(self._notebook, padding=15)
        self._notebook.add(frame, text="  Room List  ")

        ttk.Label(frame, text="All Rooms", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        cols = ("id", "type", "capacity", "bookings")
        self._room_tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        self._room_tree.heading("id", text="Room ID")
        self._room_tree.heading("type", text="Type")
        self._room_tree.heading("capacity", text="Capacity")
        self._room_tree.heading("bookings", text="Bookings")
        self._room_tree.column("id", width=100, anchor=tk.CENTER)
        self._room_tree.column("type", width=150, anchor=tk.CENTER)
        self._room_tree.column("capacity", width=100, anchor=tk.CENTER)
        self._room_tree.column("bookings", width=100, anchor=tk.CENTER)
        self._room_tree.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Refresh", command=self._refresh_room_list).pack(pady=10)

    # --- Tab 2: View Schedule ---
    def _create_schedule_tab(self):
        frame = ttk.Frame(self._notebook, padding=15)
        self._notebook.add(frame, text="  View Schedule  ")

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Room ID:").pack(side=tk.LEFT)
        self._schedule_room_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self._schedule_room_var, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="View", command=self._view_schedule).pack(side=tk.LEFT)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        self._schedule_text = tk.Text(frame, height=16, state=tk.DISABLED, font=("Courier", 10))
        self._schedule_text.pack(fill=tk.BOTH, expand=True)

    # --- Tab 3: Book a Room ---
    def _create_booking_tab(self):
        frame = ttk.Frame(self._notebook, padding=15)
        self._notebook.add(frame, text="  Book a Room  ")

        ttk.Label(frame, text="Book a Room", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, pady=10)

        # room id
        ttk.Label(form, text="Room ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._book_room_var = tk.StringVar()
        ttk.Entry(form, textvariable=self._book_room_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5)

        # weekday
        ttk.Label(form, text="Weekday:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._book_week_var = tk.StringVar()
        week_vals = [f"{k}-{v}" for k, v in sorted(WEEK_MAP.items())]
        week_cb = ttk.Combobox(form, textvariable=self._book_week_var, values=week_vals,
                               state="readonly", width=18)
        week_cb.grid(row=1, column=1, sticky=tk.W, padx=5)
        week_cb.current(0)

        # time slot
        ttk.Label(form, text="Time Slot:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self._book_slot_var = tk.StringVar()
        slot_vals = [f"{k}-{v}" for k, v in sorted(SLOT_MAP.items())]
        slot_cb = ttk.Combobox(form, textvariable=self._book_slot_var, values=slot_vals,
                               state="readonly", width=18)
        slot_cb.grid(row=2, column=1, sticky=tk.W, padx=5)
        slot_cb.current(0)

        # name
        ttk.Label(form, text="Your Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self._book_name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self._book_name_var, width=20).grid(row=3, column=1, sticky=tk.W, padx=5)

        ttk.Button(frame, text="Confirm Booking", command=self._do_booking).pack(pady=15)

    # --- Tab 4: Cancel Booking ---
    def _create_cancel_tab(self):
        frame = ttk.Frame(self._notebook, padding=15)
        self._notebook.add(frame, text="  Cancel Booking  ")

        ttk.Label(frame, text="Cancel Booking", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, pady=10)

        ttk.Label(form, text="Room ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._cancel_room_var = tk.StringVar()
        ttk.Entry(form, textvariable=self._cancel_room_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(form, text="Weekday:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._cancel_week_var = tk.StringVar()
        week_vals = [f"{k}-{v}" for k, v in sorted(WEEK_MAP.items())]
        week_cb = ttk.Combobox(form, textvariable=self._cancel_week_var, values=week_vals,
                               state="readonly", width=18)
        week_cb.grid(row=1, column=1, sticky=tk.W, padx=5)
        week_cb.current(0)

        ttk.Label(form, text="Time Slot:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self._cancel_slot_var = tk.StringVar()
        slot_vals = [f"{k}-{v}" for k, v in sorted(SLOT_MAP.items())]
        slot_cb = ttk.Combobox(form, textvariable=self._cancel_slot_var, values=slot_vals,
                               state="readonly", width=18)
        slot_cb.grid(row=2, column=1, sticky=tk.W, padx=5)
        slot_cb.current(0)

        ttk.Button(frame, text="Confirm Cancel", command=self._do_cancel).pack(pady=15)

    # --- Tab 5: Admin ---
    def _create_admin_tab(self):
        frame = ttk.Frame(self._notebook, padding=15)
        self._notebook.add(frame, text="  [Admin] Add Room  ")

        ttk.Label(frame, text="Add New Room", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, pady=10)

        ttk.Label(form, text="Room ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self._admin_id_var = tk.StringVar()
        ttk.Entry(form, textvariable=self._admin_id_var, width=20).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(form, text="Room Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self._admin_type_var = tk.StringVar()
        type_cb = ttk.Combobox(form, textvariable=self._admin_type_var,
                               values=["Classroom", "Meeting Room"], state="readonly", width=18)
        type_cb.grid(row=1, column=1, sticky=tk.W, padx=5)
        type_cb.current(0)

        ttk.Label(form, text="Capacity:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self._admin_cap_var = tk.StringVar()
        ttk.Entry(form, textvariable=self._admin_cap_var, width=20).grid(row=2, column=1, sticky=tk.W, padx=5)

        ttk.Button(frame, text="Add Room", command=self._do_add_room).pack(pady=15)

    # ========== button callbacks ==========

    def _refresh_room_list(self):
        """reload room list in the treeview"""
        for row in self._room_tree.get_children():
            self._room_tree.delete(row)
        rooms = self._manager.get_all_rooms()
        for rm in rooms:
            self._room_tree.insert("", tk.END, values=(
                rm.id, rm.room_type(), rm.capacity, len(rm.bookings)
            ))

    def _view_schedule(self):
        room_id = self._schedule_room_var.get().strip()
        if not room_id:
            messagebox.showwarning("Input Error", "Please enter a Room ID.")
            return

        room, bookings = self._manager.get_room_schedule(room_id)

        self._schedule_text.config(state=tk.NORMAL)
        self._schedule_text.delete("1.0", tk.END)

        if room is None:
            self._schedule_text.insert(tk.END, f"Room '{room_id}' not found.\n")
        else:
            self._schedule_text.insert(tk.END, f"{room.get_info()}\n")
            self._schedule_text.insert(tk.END, "-" * 40 + "\n")
            if not bookings:
                self._schedule_text.insert(tk.END, "  No bookings yet.\n")
            else:
                for ts, user in sorted(bookings.items()):
                    self._schedule_text.insert(tk.END, f"  {ts}  -  Booked by {user}\n")

        self._schedule_text.config(state=tk.DISABLED)

    def _parse_dropdown(self, week_str, slot_str):
        """parse dropdown value like '1-Mon' into time slot string"""
        w_num = week_str.split("-")[0] if "-" in week_str else ""
        s_num = slot_str.split("-")[0] if "-" in slot_str else ""
        return format_time_slot(w_num, s_num)

    def _do_booking(self):
        room_id = self._book_room_var.get().strip()
        name = self._book_name_var.get().strip()

        if not room_id:
            messagebox.showwarning("Input Error", "Please enter a Room ID.")
            return
        if not name:
            messagebox.showwarning("Input Error", "Please enter your name.")
            return

        time_slot = self._parse_dropdown(self._book_week_var.get(), self._book_slot_var.get())
        if not time_slot:
            messagebox.showerror("Error", "Invalid time selection.")
            return

        success, msg = self._manager.book_room(room_id, time_slot, name)
        if success:
            messagebox.showinfo("Success", f"Room {room_id} booked for [{time_slot}].")
            self._refresh_room_list()
        else:
            messagebox.showerror("Booking Failed", msg)

    def _do_cancel(self):
        room_id = self._cancel_room_var.get().strip()
        if not room_id:
            messagebox.showwarning("Input Error", "Please enter a Room ID.")
            return

        time_slot = self._parse_dropdown(self._cancel_week_var.get(), self._cancel_slot_var.get())
        if not time_slot:
            messagebox.showerror("Error", "Invalid time selection.")
            return

        success, msg = self._manager.cancel_booking(room_id, time_slot)
        if success:
            messagebox.showinfo("Success", f"Booking for [{time_slot}] cancelled.")
            self._refresh_room_list()
        else:
            messagebox.showwarning("Cancel Failed", msg)

    def _do_add_room(self):
        new_id = self._admin_id_var.get().strip()
        cap_str = self._admin_cap_var.get().strip()
        room_type = self._admin_type_var.get()

        if not new_id:
            messagebox.showwarning("Input Error", "Please enter a Room ID.")
            return
        if not cap_str.isdigit() or int(cap_str) <= 0:
            messagebox.showwarning("Input Error", "Capacity must be a positive integer.")
            return

        success, msg = self._manager.add_room(new_id, int(cap_str), room_type)
        if success:
            messagebox.showinfo("Success", f"Room '{new_id}' added as {room_type}.")
            self._refresh_room_list()
            self._admin_id_var.set("")
            self._admin_cap_var.set("")
        else:
            messagebox.showwarning("Failed", msg)
