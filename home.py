import tkinter as tk
from tkinter import ttk

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="Flight Reservation System", font=('Arial', 16))
        label.pack(pady=40)
 
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        book_button = ttk.Button(
            button_frame, 
            text="Book Flight", 
            width=20,
            command=lambda: controller.show_frame("BookingPage")
        )
        book_button.pack(pady=10)

        view_button = ttk.Button(
            button_frame, 
            text="View Reservations", 
            width=20,
            command=lambda: controller.show_frame("ReservationsPage")
        )
        view_button.pack(pady=10)