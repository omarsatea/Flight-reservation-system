import tkinter as tk
from tkinter import messagebox
from home import HomePage
from booking import BookingPage
from reservations import ReservationsPage
from edit_reservation import EditPage

class FlightReservationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flight Reservation System")
        self.geometry("800x600")
        
        # Container for frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Register all pages except EditPage
        for F in (HomePage, BookingPage, ReservationsPage):
            page_name = F.__name__
            frame = F(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Initialize EditPage placeholder
        self.frames["EditPage"] = None
        
        self.show_frame("HomePage")

    def show_frame(self, page_name, *args):
        """Show a frame for the given page name."""
        # Special handling for EditPage
        if page_name == "EditPage":
            if not args:
                messagebox.showerror("Error", "No reservation selected!")
                return
            
            if self.frames["EditPage"] is None:
                self.frames["EditPage"] = EditPage(self.container, self, args[0])
                self.frames["EditPage"].grid(row=0, column=0, sticky="nsew")
            else:
                self.frames["EditPage"].reservation_id = args[0]
                self.frames["EditPage"].load_reservation()
        
        # Raise the requested frame
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Refresh if it's ReservationsPage
        if page_name == "ReservationsPage":
            frame.refresh_reservations()

if __name__ == "__main__":
    app = FlightReservationApp()
    app.mainloop()