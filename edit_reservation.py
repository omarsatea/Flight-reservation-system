import tkinter as tk
from tkinter import messagebox
from database import create_connection

class EditPage(tk.Frame):
    def __init__(self, parent, controller, reservation_id=None):
        super().__init__(parent)
        self.controller = controller
        self.reservation_id = reservation_id
        
        # Form frame
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20)
        
        fields = ["Name", "Flight Number", "Departure", "Destination", "Date", "Seat Number"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field+":").grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        update_btn = tk.Button(
            button_frame, 
            text="Update Reservation",
            command=self.update_reservation,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        update_btn.pack(side='left', padx=10)
        
        delete_btn = tk.Button(
            button_frame, 
            text="Delete Reservation",
            command=self.delete_reservation,
            bg="#f44336",
            fg="white",
            padx=10,
            pady=5
        )
        delete_btn.pack(side='left', padx=10)
        
        back_btn = tk.Button(
            button_frame,
            text="Back to List",
            command=lambda: controller.show_frame("ReservationsPage"),
            padx=10,
            pady=5
        )
        back_btn.pack(side='left', padx=10)
        
        if self.reservation_id:
            self.load_reservation()

    def load_reservation(self):
        """Load reservation data into form."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM reservations WHERE id=?", (self.reservation_id,))
                row = cursor.fetchone()
                
                if row:
                    for entry in self.entries.values():
                        entry.delete(0, tk.END)
                    
                    self.entries["Name"].insert(0, row[1])
                    self.entries["Flight Number"].insert(0, row[2])
                    self.entries["Departure"].insert(0, row[3])
                    self.entries["Destination"].insert(0, row[4])
                    self.entries["Date"].insert(0, row[5])
                    self.entries["Seat Number"].insert(0, row[6])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data:\n{str(e)}")
            finally:
                conn.close()

    def update_reservation(self):
        """Handle update button click."""
        if not self.reservation_id:
            messagebox.showerror("Error", "No reservation selected!")
            return
            
        conn = None
        try:
            values = (
                self.entries["Name"].get().strip(),
                self.entries["Flight Number"].get().strip(),
                self.entries["Departure"].get().strip(),
                self.entries["Destination"].get().strip(),
                self.entries["Date"].get().strip(),
                self.entries["Seat Number"].get().strip(),
                self.reservation_id
            )
            
            if not all(values[:-1]):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE reservations 
                SET name=?, flight_number=?, departure=?,
                    destination=?, date=?, seat_number=?
                WHERE id=?
            ''', values)
            conn.commit()
            
            conn.close()
            conn = None
            
            self.controller.show_frame("ReservationsPage")
            
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{str(e)}")
        finally:
            if conn:
                conn.close()

    def delete_reservation(self):
        """Handle delete button click."""
        if not self.reservation_id:
            messagebox.showerror("Error", "No reservation selected!")
            return
            
        if messagebox.askyesno("Confirm Delete", "Delete this reservation permanently?"):
            conn = None
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM reservations WHERE id=?", (self.reservation_id,))
                conn.commit()
                messagebox.showinfo("Success", "Reservation deleted!")
                self.controller.show_frame("ReservationsPage")
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed:\n{str(e)}")
            finally:
                if conn:
                    conn.close()