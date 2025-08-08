import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection

class ReservationsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Flight", "Departure", "Destination", "Date", "Seat"), 
                                show="headings", yscrollcommand=scrollbar.set)
        
        # Configure columns
        columns = ["ID", "Name", "Flight", "Departure", "Destination", "Date", "Seat"]
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Bind double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        refresh_btn = tk.Button(button_frame, text="Refresh", command=self.refresh_reservations)
        refresh_btn.pack(side='left', padx=5)
        
        back_btn = tk.Button(button_frame, text="Back", command=lambda: controller.show_frame("HomePage"))
        back_btn.pack(side='left', padx=5)
        
        self.refresh_reservations()

    def refresh_reservations(self):
        """Refresh the reservations list from database"""
        self.tree.delete(*self.tree.get_children())
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM reservations ORDER BY date DESC")
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to refresh: {e}")
            finally:
                conn.close()

    def on_double_click(self, event):
        """Handle double click to edit reservation."""
        item = self.tree.selection()[0]
        reservation_id = self.tree.item(item, "values")[0]
        self.controller.show_frame("EditPage", reservation_id)