import tkinter as tk
from tkinter import ttk, messagebox
import snap7
import csv
from datetime import datetime
import struct

class PLCDataLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Siemens PLC Data Logger")
        self.root.geometry("500x300")
        
        # PLC Connection Variables
        self.plc_ip = tk.StringVar()
        self.db_number = tk.IntVar(value=1)
        self.rack = tk.IntVar(value=0)
        self.slot = tk.IntVar(value=1)
        
        # Create GUI elements
        self.create_widgets()
        
        # PLC client instance
        self.plc = snap7.client.Client()
        
    def create_widgets(self):
        # Connection Frame
        connection_frame = ttk.LabelFrame(self.root, text="PLC Connection Settings", padding=10)
        connection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # IP Address
        ttk.Label(connection_frame, text="PLC IP Address:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.plc_ip).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # DB Number
        ttk.Label(connection_frame, text="DB Number:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.db_number).grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Rack and Slot
        ttk.Label(connection_frame, text="Rack:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.rack).grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(connection_frame, text="Slot:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(connection_frame, textvariable=self.slot).grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(self.root, padding=10)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Connect Button
        ttk.Button(buttons_frame, text="Connect to PLC", command=self.connect_to_plc).pack(side=tk.LEFT, padx=5)
        
        # Read DB Button
        self.read_button = ttk.Button(buttons_frame, text="Read DB and Save to CSV", command=self.read_db_and_save, state=tk.DISABLED)
        self.read_button.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = ttk.Label(self.root, text="Not connected to PLC", foreground="red")
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Log Text
        self.log_text = tk.Text(self.root, height=8, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def connect_to_plc(self):
        ip_address = self.plc_ip.get()
        if not ip_address:
            messagebox.showerror("Error", "Please enter PLC IP address")
            return
            
        try:
            self.plc.connect(ip_address, self.rack.get(), self.slot.get())
            if self.plc.get_connected():
                self.status_label.config(text=f"Connected to PLC at {ip_address}", foreground="green")
                self.read_button.config(state=tk.NORMAL)
                self.log_message(f"Successfully connected to PLC at {ip_address}")
            else:
                self.status_label.config(text="Failed to connect to PLC", foreground="red")
                self.log_message("Failed to connect to PLC")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to PLC: {str(e)}")
            self.log_message(f"Connection error: {str(e)}")
            
    def read_db_and_save(self):
        if not self.plc.get_connected():
            messagebox.showerror("Error", "Not connected to PLC")
            return
            
        db_number = self.db_number.get()
        try:
            # Get DB information
            db_info = self.plc.db_get(db_number)
            db_size = db_info[2]
            
            # Read entire DB
            db_data = self.plc.db_read(db_number, 0, db_size)
            
            # Create CSV filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"plc_db{db_number}_data_{timestamp}.csv"
            
            # Try to parse the data (this is a simple example - you'll need to customize based on your DB structure)
            # For demonstration, we'll just save the raw bytes and some interpreted values
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Byte Offset', 'Raw Byte', 'As Bool', 'As Int', 'As Float'])
                
                # Write data
                for i in range(db_size):
                    byte = db_data[i]
                    bool_val = bool(byte)
                    
                    # Try to read as int (16-bit)
                    int_val = ''
                    if i + 1 < db_size:
                        int_val = struct.unpack_from('>h', db_data, i)[0]
                        
                    # Try to read as float (32-bit)
                    float_val = ''
                    if i + 3 < db_size:
                        float_val = struct.unpack_from('>f', db_data, i)[0]
                        
                    writer.writerow([i, byte, bool_val, int_val, float_val])
            
            self.log_message(f"Successfully read DB{db_number} and saved to {filename}")
            messagebox.showinfo("Success", f"Data saved to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read DB: {str(e)}")
            self.log_message(f"Error reading DB: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PLCDataLogger(root)
    root.mainloop()