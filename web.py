import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import pandas as pd

class AttendanceDB:
    def __init__(self):
        self.students = {
            "RFID001": {"name": "John Doe", "id": "S001", "status": "Valid"},
            "RFID002": {"name": "Jane Smith", "id": "S002", "status": "Valid"},
            "RFID003": {"name": "Mike Johnson", "id": "S003", "status": "Valid"},
        }
        self.attendance_log = []
        self.pending_requests = []

    def log_attendance(self, rfid, name, status):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "rfid": rfid, "name": name, "status": status}
        self.attendance_log.append(entry)
        return entry

    def get_student(self, rfid):
        return self.students.get(rfid, None)

    def add_pending_request(self, rfid):
        if rfid not in [req['rfid'] for req in self.pending_requests]:
            self.pending_requests.append({
                "rfid": rfid,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return True
        return False

    def approve_pending_request(self, rfid):
        for i, req in enumerate(self.pending_requests):
            if req['rfid'] == rfid:
                self.pending_requests.pop(i)
                self.students[rfid] = {
                    "name": "New Student",
                    "id": f"S{len(self.students)+1:03d}",
                    "status": "Valid"
                }
                return True
        return False

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System - Admin Portal")
        self.root.geometry("1200x800")
        self.db = AttendanceDB()
        self.create_widgets()
        self.setup_demo_controls()

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.theme_use("clam")

        # Fonts and Colors for Modern Feel
        style.configure("Treeview.Heading",
                        background="#e4f2f4",
                        foreground="#333",
                        font=('Helvetica', 12, 'bold'))
        style.configure("Treeview",
                        background="#f9f9f9",
                        foreground="black",
                        fieldbackground="#f9f9f9",
                        rowheight=30)

        style.map('Treeview', background=[('selected', '#d9ecf2')])

        # Layout
        self.top_frame = ttk.Frame(self.root, padding="10", relief="flat", style="TFrame")
        self.top_frame.pack(fill=tk.X)

        self.middle_frame = ttk.Frame(self.root, padding="10", relief="flat", style="TFrame")
        self.middle_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = ttk.Frame(self.root, padding="10", relief="flat", style="TFrame")
        self.bottom_frame.pack(fill=tk.X)

        # Header
        ttk.Label(self.top_frame, text="Smart Attendance System", font=('Helvetica', 20, 'bold'), foreground="#4c4c4c").pack(pady=10)

        self.scan_info_frame = ttk.LabelFrame(self.top_frame, text="Latest Scan Info", padding="10")
        self.scan_info_frame.pack(fill=tk.X, pady=10)

        self.scan_info_text = tk.StringVar()
        self.scan_info_text.set("No scan detected yet")
        ttk.Label(self.scan_info_frame, textvariable=self.scan_info_text, font=('Helvetica', 14)).pack()

        self.notebook = ttk.Notebook(self.middle_frame)

        # Tabs
        self.create_log_tab()
        self.create_students_tab()
        self.create_pending_tab()

        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Footer Controls
        ttk.Button(self.bottom_frame, text="Refresh Data", command=self.refresh_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.bottom_frame, text="Export to Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.bottom_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=10)

        self.refresh_data()

    def create_log_tab(self):
        self.log_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.log_tab, text="Attendance Log")

        self.log_tree = ttk.Treeview(self.log_tab, columns=("Timestamp", "RFID", "Name", "Status"), show="headings")
        for col in ("Timestamp", "RFID", "Name", "Status"):
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=200, anchor=tk.CENTER)
        self.log_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_students_tab(self):
        self.students_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.students_tab, text="Student Database")

        self.students_tree = ttk.Treeview(self.students_tab, columns=("RFID", "Name", "ID", "Status"), show="headings")
        for col in ("RFID", "Name", "ID", "Status"):
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150, anchor=tk.CENTER)
        self.students_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_pending_tab(self):
        self.pending_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pending_tab, text="Pending Requests")

        self.pending_tree = ttk.Treeview(self.pending_tab, columns=("Timestamp", "RFID"), show="headings")
        for col in ("Timestamp", "RFID"):
            self.pending_tree.heading(col, text=col)
            self.pending_tree.column(col, width=250, anchor=tk.CENTER)
        self.pending_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.approve_btn = ttk.Button(self.pending_tab, text="Approve Selected", command=self.approve_request)
        self.approve_btn.pack(pady=5)

    def setup_demo_controls(self):
        demo_frame = ttk.LabelFrame(self.bottom_frame, text="Simulate RFID Scan", padding="10")
        demo_frame.pack(side=tk.RIGHT, padx=10)

        self.demo_rfid_entry = ttk.Entry(demo_frame, width=15, font=('Helvetica', 12))
        self.demo_rfid_entry.pack(side=tk.LEFT, padx=5)
        self.demo_rfid_entry.insert(0, "RFID001")

        ttk.Button(demo_frame, text="Scan", command=self.simulate_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(demo_frame, text="Invalid Scan", command=self.simulate_invalid_scan).pack(side=tk.LEFT, padx=5)

    def simulate_scan(self):
        rfid = self.demo_rfid_entry.get()
        self.process_rfid_scan(rfid)

    def simulate_invalid_scan(self):
        rfid = "INVALID_" + str(len(self.db.pending_requests) + 1)
        self.demo_rfid_entry.delete(0, tk.END)
        self.demo_rfid_entry.insert(0, rfid)
        self.process_rfid_scan(rfid)

    def process_rfid_scan(self, rfid):
        student = self.db.get_student(rfid)
        if student:
            entry = self.db.log_attendance(rfid, student['name'], "Present")
            self.scan_info_text.set(f"Valid scan: {student['name']} ({student['id']}) - {entry['timestamp']}")
        else:
            if self.db.add_pending_request(rfid):
                self.scan_info_text.set(f"Unknown RFID: {rfid} - Added to pending requests")
            else:
                self.scan_info_text.set(f"Unknown RFID: {rfid} - Already in pending requests")
        self.refresh_data()

    def approve_request(self):
        selected = self.pending_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a request to approve")
            return
        item = self.pending_tree.item(selected[0])
        rfid = item['values'][1]
        if self.db.approve_pending_request(rfid):
            messagebox.showinfo("Success", f"RFID {rfid} approved and added to student database")
            self.refresh_data()
        else:
            messagebox.showerror("Error", "Failed to approve the request")

    def refresh_data(self):
        # Attendance log
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        for entry in self.db.attendance_log:
            self.log_tree.insert("", tk.END, values=(entry['timestamp'], entry['rfid'], entry.get('name', ''), entry['status']))

        # Student database
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        for i, (rfid, student) in enumerate(self.db.students.items()):
            self.students_tree.insert("", tk.END, values=(rfid, student['name'], student['id'], student['status']))

        # Pending requests
        for item in self.pending_tree.get_children():
            self.pending_tree.delete(item)
        for request in self.db.pending_requests:
            self.pending_tree.insert("", tk.END, values=(request['timestamp'], request['rfid']))

    def export_to_excel(self):
        if not self.db.attendance_log:
            messagebox.showwarning("No Data", "There is no attendance data to export")
            return
        df = pd.DataFrame(self.db.attendance_log)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"attendance_export_{timestamp}.xlsx"
        df.to_excel(filename, index=False)
        messagebox.showinfo("Export Successful", f"Attendance data exported to {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
