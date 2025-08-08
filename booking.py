import tkinter as tk
from tkinter import messagebox
from database import create_connection
from home import HomePage
from sqlite3 import Error

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
       
        fields = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(self, text=field).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        
        submit_btn = tk.Button(self, text="Submit", command=self.submit)
        submit_btn.grid(row=len(fields), column=0, pady=10)
        
        back_btn = tk.Button(self, text="Back", command=lambda: controller.show_frame("HomePage"))
        back_btn.grid(row=len(fields), column=1, pady=10)

    def submit(self):
        """Save reservation to database."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO reservations (name, flight_number, departure, destination, date, seat_number)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.entries["Name"].get(),
                    self.entries["Flight Number"].get(),
                    self.entries["Departure"].get(),
                    self.entries["Destination"].get(),
                    self.entries["Date"].get(),
                    self.entries["Seat Number"].get()
                ))
                conn.commit()
                messagebox.showinfo("Success", "Reservation booked!")
                self.controller.show_frame(HomePage)
            except Error as e:
                messagebox.showerror("Error", f"Failed to book: {e}")
            finally:
                conn.close()