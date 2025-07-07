import tkinter as tk
from tkinter import ttk, messagebox, font
import time
from datetime import datetime
import random
import os
from PIL import Image, ImageTk  # Install with: pip install pillow

class SmartAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System")
        self.root.geometry("1000x600")
        self.root.config(bg="#f5f7fa")
        self.root.resizable(True, True)

        # Create custom styles
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Colors
        self.primary = "#4361ee"
        self.secondary = "#3f37c9"
        self.accent = "#4cc9f0"
        self.dark = "#1a1a2e"
        self.light = "#f8f9fa"
        self.error = "#e63946"
        self.success = "#2a9d8f"

        # Configure styles
        self.style.configure("TButton",
                           font=("Segoe UI", 10, "bold"),
                           background=self.primary,
                           foreground="white")

        self.style.map("TButton",
                     background=[("active", self.secondary),
                                 ("disabled", "#cccccc")])

        self.style.configure("TEntry",
                           font=("Segoe UI", 10),
                           background="white")

        self.style.configure("TFrame", background=self.light)

        # Initialize frames
        self.login_frame = None
        self.dashboard_frame = None
        self.current_frame = None

        # Create login window
        self.create_login_window()

    def create_login_window(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.current_frame = self.login_frame

        # Header with gradient
        header_frame = ttk.Frame(self.login_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        header_bg = tk.Canvas(header_frame, height=80, bg=self.primary, highlightthickness=0)
        header_bg.pack(fill=tk.X)

        for i in range(80):
            r1, g1, b1 = tuple(int(self.primary[1:][i:i+2], 16) for i in (0, 2, 4))
            r2, g2, b2 = tuple(int(self.secondary[1:][i:i+2], 16) for i in (0, 2, 4))
            r = int(r1 + (r2-r1) * i / 80)
            g = int(g1 + (g2-g1) * i / 80)
            b = int(b1 + (b2-b1) * i / 80)
            color = f'#{r:02x}{g:02x}{b:02x}'
            header_bg.create_line(0, i, 1000, i, fill=color)

        tk.Label(header_bg, text="Smart Attendance Solution",
                font=("Segoe UI", 18, "bold"), fg="white", bg=self.primary).place(relx=0.03, rely=0.3)
        tk.Label(header_bg, text="Contactless RFID technology for accurate, real-time attendance tracking",
                font=("Segoe UI", 10), fg="white", bg=self.primary).place(relx=0.03, rely=0.7)

        # Main content
        content_frame = ttk.Frame(self.login_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Form section
        form_frame = ttk.Frame(content_frame, padding=40)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        form_center = ttk.Frame(form_frame)
        form_center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(form_center, text="Admin Login",
               font=("Segoe UI", 22, "bold"), fg=self.dark).pack(anchor=tk.W, pady=(0, 10))
        tk.Label(form_center, text="Enter your credentials to access the system",
               font=("Segoe UI", 10), fg="#666666").pack(anchor=tk.W, pady=(0, 30))

        # Error message
        self.error_message = tk.Label(form_center, text="Invalid credentials",
                                    font=("Segoe UI", 10), fg="white", bg=self.error,
                                    padx=10, pady=10)

        # Username field
        tk.Label(form_center, text="Username", font=("Segoe UI", 10, "bold"), fg="#333333").pack(anchor=tk.W, pady=(0, 5))
        self.username_var = tk.StringVar()
        ttk.Entry(form_center, textvariable=self.username_var, width=30, font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 15), ipady=5)

        # Password field
        tk.Label(form_center, text="Password", font=("Segoe UI", 10, "bold"), fg="#333333").pack(anchor=tk.W, pady=(0, 5))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_center, textvariable=self.password_var, show="•", width=30, font=("Segoe UI", 10))
        password_entry.pack(anchor=tk.W, pady=(0, 15), ipady=5)
        password_entry.bind('<Return>', lambda e: self.login())

        # Login button
        tk.Button(form_center, text="Login to Dashboard",
                font=("Segoe UI", 12, "bold"), bg=self.primary, fg="white",
                activebackground=self.secondary, padx=10, pady=8, borderwidth=0,
                command=self.login).pack(fill=tk.X, pady=(20, 0))

        # Image section
        image_frame = ttk.Frame(content_frame, style="Image.TFrame")
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.style.configure("Image.TFrame", background=self.primary)

    def login(self):
        if self.username_var.get() == "admin" and self.password_var.get() == "password":
            self.create_dashboard()
        else:
            self.error_message.pack()
            self.root.after(3000, lambda: self.error_message.pack_forget())

    def create_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.current_frame = self.dashboard_frame

        # Header
        header_frame = ttk.Frame(self.dashboard_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        header_bg = tk.Canvas(header_frame, height=80, bg=self.primary, highlightthickness=0)
        header_bg.pack(fill=tk.X)

        # Gradient effect
        for i in range(80):
            r1, g1, b1 = tuple(int(self.primary[1:][i:i+2], 16) for i in (0, 2, 4))
            r2, g2, b2 = tuple(int(self.secondary[1:][i:i+2], 16) for i in (0, 2, 4))
            r = int(r1 + (r2-r1) * i / 80)
            g = int(g1 + (g2-g1) * i / 80)
            b = int(b1 + (b2-b1) * i / 80)
            color = f'#{r:02x}{g:02x}{b:02x}'
            header_bg.create_line(0, i, 1000, i, fill=color)

        tk.Label(header_bg, text="Smart Attendance Dashboard",
                font=("Segoe UI", 18, "bold"), fg="white", bg=self.primary).place(relx=0.03, rely=0.3)
        tk.Label(header_bg, text="Live monitoring and management",
                font=("Segoe UI", 10), fg="white", bg=self.primary).place(relx=0.03, rely=0.7)

        # Main content
        content_frame = ttk.Frame(self.dashboard_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Stats cards
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        stats = [
            {"value": "142", "label": "Present Today"},
            {"value": "8", "label": "Absent Today"},
            {"value": "94%", "label": "Attendance Rate"},
            {"value": "1.2s", "label": "Avg. Scan Time"}
        ]

        for i, stat in enumerate(stats):
            card = tk.Frame(stats_frame, bg="white", padx=15, pady=15,
                          highlightbackground="#eeeeee", highlightthickness=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            stats_frame.columnconfigure(i, weight=1)

            tk.Label(card, text=stat["value"], font=("Segoe UI", 22, "bold"), fg=self.primary, bg="white").pack()
            tk.Label(card, text=stat["label"], font=("Segoe UI", 9), fg="#666666", bg="white").pack()

        # Scanner simulation
        scanner_frame = ttk.Frame(content_frame)
        scanner_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(scanner_frame, text="RFID Scanner Simulation", font=("Segoe UI", 12, "bold")).pack(pady=10)
        
        scan_btn = tk.Button(scanner_frame, text="Simulate RFID Scan", bg=self.primary, fg="white",
                           font=("Segoe UI", 12), command=self.simulate_scan)
        scan_btn.pack(pady=20)

        self.scan_result = tk.Label(scanner_frame, text="", font=("Segoe UI", 12))
        self.scan_result.pack()

    def simulate_scan(self):
        students = {
            "RFID001": "John Doe",
            "RFID002": "Jane Smith",
            "RFID003": "Mike Johnson"
        }
        rfid = random.choice(list(students.keys()))
        self.scan_result.config(text=f"Scanned: {students[rfid]} ({rfid})", fg=self.success)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAttendanceSystem(root)
    root.mainloop()