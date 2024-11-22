import sqlite3
import tkinter as tk
from tkinter import messagebox

# Step 1: Database Setup
def initialize_database():
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    
    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        action_taken TEXT,
        timestamp TIMESTAMP,
        password TEXT
    )''')

    # Create Cables table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cables (
        cable_id INTEGER PRIMARY KEY,
        type TEXT,
        length INTEGER,
        status TEXT,
        location TEXT
    )''')
    
    # Create Connections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Connections (
        connection_id INTEGER PRIMARY KEY,
        cable_id INTEGER,
        device_port TEXT,
        connected_to TEXT,
        connection_status TEXT,
        timestamp TIMESTAMP,
        FOREIGN KEY (cable_id) REFERENCES Cables (cable_id)
    )''')
    
    # Create History table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS History (
        history_id INTEGER PRIMARY KEY,
        cable_id INTEGER,
        action TEXT,
        location TEXT,
        timestamp TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (cable_id) REFERENCES Cables (cable_id)
    )''')

    conn.commit()
    conn.close()

# Step 2: Login and Signup Functions
def login(username, password):
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", "Welcome back!")
        home_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def signup(username, password):
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Signup Success", "User created successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Signup Failed", "Username already exists")
    finally:
        conn.close()

# Step 3: Tkinter Interface for Login and Signup
def login_signup():
    def login_action():
        login(username_entry.get(), password_entry.get())

    def signup_action():
        signup(username_entry.get(), password_entry.get())
    
    login_window = tk.Tk()
    login_window.title("Login or Signup")

    # Set window size (width x height)
    login_window.geometry("300x300")  # Adjust the size as needed

    # Create a frame for better organization
    frame = tk.Frame(login_window)
    frame.pack(pady=20)  # Adds vertical padding around the frame

    # Username Label and Entry
    tk.Label(frame, text="Username:").pack(pady=5)
    username_entry = tk.Entry(frame)
    username_entry.pack(pady=5)

    # Password Label and Entry
    tk.Label(frame, text="Password:").pack(pady=5)
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    # Login and Signup Buttons with padding
    tk.Button(frame, text="Login", command=login_action).pack(pady=10)
    tk.Button(frame, text="Signup", command=signup_action).pack(pady=10)

    login_window.mainloop()

def home_menu():
    home_window = tk.Tk()
    home_window.title("Home Menu")

    # Set window size (width x height)
    home_window.geometry("400x500")  # Adjust the size as needed

    # Create a frame for better organization
    frame = tk.Frame(home_window)
    frame.pack(pady=20)  # Adds vertical padding around the frame

    # Buttons for each feature with padding
    tk.Button(frame, text="View Cables", command=view_cables, width=20).pack(pady=5)
    tk.Button(frame, text="Add Cable", command=add_cable, width=20).pack(pady=5)
    tk.Button(frame, text="View Connections", command=view_connections, width=20).pack(pady=5)
    tk.Button(frame, text="Add Connection", command=add_connection, width=20).pack(pady=5)
    tk.Button(frame, text="View History", command=view_history, width=20).pack(pady=5)
    tk.Button(frame, text="Add History", command=add_history, width=20).pack(pady=5)
    tk.Button(frame, text="Delete Cable", command=delete_cable, width=20).pack(pady=5)
    tk.Button(frame, text="Delete Connection", command=delete_connection, width=20).pack(pady=5)
    tk.Button(frame, text="Exit", command=home_window.destroy, width=20).pack(pady=5)

    home_window.mainloop()

    
# Step 4: View Cables Function
def view_cables():
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cables')
    cables = cursor.fetchall()
    conn.close()

    view_window = tk.Tk()
    view_window.title("View Cables")

    for cable in cables:
        tk.Label(view_window, text=str(cable)).pack()

    view_window.mainloop()


# Step 5: Add Cable Function
def add_cable():
    add_window = tk.Tk()
    add_window.title("Add Cable")

    tk.Label(add_window, text="Cable Type:").pack()
    type_entry = tk.Entry(add_window)
    type_entry.pack()

    tk.Label(add_window, text="Cable Length (m):").pack()
    length_entry = tk.Entry(add_window)
    length_entry.pack()

    tk.Label(add_window, text="Status:").pack()
    status_entry = tk.Entry(add_window)
    status_entry.pack()

    tk.Label(add_window, text="Location:").pack()
    location_entry = tk.Entry(add_window)
    location_entry.pack()

    def save_cable():
        conn = sqlite3.connect('cables_management.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Cables (type, length, status, location) VALUES (?, ?, ?, ?)',
                       (type_entry.get(), length_entry.get(), status_entry.get(), location_entry.get()))
        cursor.execute('''
            INSERT INTO History (cable_id, action, location, timestamp, notes)
            VALUES (?, ?, ?, datetime('now'), ?)
        ''', (cursor.lastrowid, "Added Cable", "Unknown", "Cable added to system."))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Cable added successfully!")
        add_window.destroy()

    tk.Button(add_window, text="Save", command=save_cable).pack()
    add_window.mainloop()

# Step 6: View Connections Function
def view_connections():
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Connections')
    connections = cursor.fetchall()
    conn.close()

    view_window = tk.Tk()
    view_window.title("View Connections")

    for connection in connections:
        tk.Label(view_window, text=str(connection)).pack()

    view_window.mainloop()
    
# Step 7: Add Connections Function
def add_connection():
    connection_window = tk.Tk()
    connection_window.title("Add Connection")

    # Input fields
    tk.Label(connection_window, text="Cable ID:").pack()
    cable_id_entry = tk.Entry(connection_window)
    cable_id_entry.pack()

    tk.Label(connection_window, text="Device Port:").pack()
    device_port_entry = tk.Entry(connection_window)
    device_port_entry.pack()

    tk.Label(connection_window, text="Connected To:").pack()
    connected_to_entry = tk.Entry(connection_window)
    connected_to_entry.pack()

    tk.Label(connection_window, text="Connection Status:").pack()
    status_entry = tk.Entry(connection_window)
    status_entry.pack()

    def save_connection():
        conn = sqlite3.connect('cables_management.db')
        cursor = conn.cursor()
        
        # Insert into Connections table
        cursor.execute('''
            INSERT INTO Connections (cable_id, device_port, connected_to, connection_status, timestamp)
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (cable_id_entry.get(), device_port_entry.get(), connected_to_entry.get(), status_entry.get()))
        
        # Log the action in the History table
        cursor.execute('''
            INSERT INTO History (cable_id, action, location, timestamp, notes)
            VALUES (?, ?, ?, datetime('now'), ?)
        ''', (cable_id_entry.get(), "Added Connection", "Unknown", "Connection added to device."))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Connection added successfully!")
        connection_window.destroy()

    # Button to save connection
    tk.Button(connection_window, text="Save Connection", command=save_connection).pack()
    connection_window.mainloop()


# Step 8: View History Function
def view_history():
    history_window = tk.Tk()
    history_window.title("Connection History")

    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM History')
    history_records = cursor.fetchall()
    conn.close()

    # Display each record
    for record in history_records:
        tk.Label(history_window, text=str(record)).pack()

    history_window.mainloop()

# Step 9: Log changes in history
def add_history(cable_id, action, location, notes):
    conn = sqlite3.connect('cables_management.db')
    cursor = conn.cursor()
    
    # Insert a new history record
    cursor.execute('''
        INSERT INTO History (cable_id, action, location, timestamp, notes)
        VALUES (?, ?, ?, datetime('now'), ?)
    ''', (cable_id, action, location, notes))
    
    conn.commit()
    conn.close()

# Step 10: Delete Cable Function
def delete_cable():
    delete_window = tk.Tk()
    delete_window.title("Delete Cable")

    tk.Label(delete_window, text="Cable ID:").pack()
    cable_id_entry = tk.Entry(delete_window)
    cable_id_entry.pack()

    def confirm_delete():
        conn = sqlite3.connect('cables_management.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Cables WHERE cable_id = ?', (cable_id_entry.get(),))
        conn.commit()
        if cursor.rowcount > 0:
            add_history(cable_id_entry.get(), "Deleted Cable", "Unknown", "Cable deleted from the system.")
            messagebox.showinfo("Success", "Cable deleted successfully!")
        else:
            messagebox.showerror("Error", "Cable ID not found!")
        conn.close()
        delete_window.destroy()

    tk.Button(delete_window, text="Delete Cable", command=confirm_delete).pack()
    delete_window.mainloop()

# Step 11: Delete Connection Function
def delete_connection():
    delete_window = tk.Tk()
    delete_window.title("Delete Connection")

    tk.Label(delete_window, text="Connection ID:").pack()
    connection_id_entry = tk.Entry(delete_window)
    connection_id_entry.pack()

    def confirm_delete():
        conn = sqlite3.connect('cables_management.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Connections WHERE connection_id = ?', (connection_id_entry.get(),))
        conn.commit()
        if cursor.rowcount > 0:
            add_history(connection_id_entry.get(), "Deleted Connection", "Unknown", "Connection deleted from the system.")
            messagebox.showinfo("Success", "Connection deleted successfully!")
        else:
            messagebox.showerror("Error", "Connection ID not found!")
        conn.close()
        delete_window.destroy()

    tk.Button(delete_window, text="Delete Connection", command=confirm_delete).pack()
    delete_window.mainloop()


# Initialize Database and Start Login
initialize_database()
login_signup()