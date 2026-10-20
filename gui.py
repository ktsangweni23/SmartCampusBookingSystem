from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

from database import campus_report, cross_campus_report

DB_NAME = "campus.db"


# ==========================
# LOGIN WINDOW
# ==========================

class LoginWindow(Tk):

    def __init__(self):
        super().__init__()

        self.title("Smart Campus Booking System")
        self.geometry("500x400")

        Label(self, text="Username").pack(pady=5)

        self.username = Entry(self)
        self.username.pack()

        Label(self, text="Password").pack(pady=5)

        self.password = Entry(self, show="*")
        self.password.pack()

        Button(
            self,
            text="Login",
            command=self.login
        ).pack(pady=10)

        Button(
            self,
            text="Register",
            command=self.register
        ).pack(pady=10)

    def login(self):

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, role
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (
                self.username.get(),
                self.password.get()
            )
        )

        result = cursor.fetchone()

        conn.close()

        if result:

            messagebox.showinfo(
                "Success",
                "Login Successful"
            )

            Dashboard(result[0], result[1])

        else:

            messagebox.showerror(
                "Error",
                "Invalid Login"
            )

    def register(self):
        RegisterWindow()


# ==========================
# REGISTER WINDOW
# ==========================

class RegisterWindow(Toplevel):

    def __init__(self):
        super().__init__()

        self.title("Register")
        self.geometry("400x300")

        Label(self, text="Username").pack()

        self.username = Entry(self)
        self.username.pack()

        Label(self, text="Password").pack()

        self.password = Entry(self, show="*")
        self.password.pack()

        Label(self, text="Role").pack()

        self.role = ttk.Combobox(
            self,
            values=[
                "Lecturer",
                "CampusAdmin",
                "SystemOperator"
            ]
        )

        self.role.pack()

        Button(
            self,
            text="Create Account",
            command=self.save
        ).pack(pady=10)

    def save(self):

        try:

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (username, password, role)
                VALUES (?, ?, ?)
                """,
                (
                    self.username.get(),
                    self.password.get(),
                    self.role.get()
                )
            )

            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Account Created"
            )

            self.destroy()

        except:

            messagebox.showerror(
                "Error",
                "User already exists"
            )


# ==========================
# DASHBOARD
# ==========================

class Dashboard(Toplevel):

    def __init__(self, user_id, role):
        super().__init__()

        self.user_id = user_id
        self.role = role

        self.title("Dashboard")
        self.geometry("800x500")

        Label(
            self,
            text=f"Logged in as: {role}",
            font=("Arial", 14)
        ).pack(pady=10)

        Button(
            self,
            text="Book Resource",
            command=self.book_resource
        ).pack(pady=5)

        Button(
            self,
            text="Campus Report",
            command=self.show_report
        ).pack(pady=5)

        Button(
            self,
            text="Cross Campus Report",
            command=self.show_cross_report
        ).pack(pady=5)

    def book_resource(self):
        BookingWindow(self.user_id)

    def show_report(self):

        report = campus_report()

        messagebox.showinfo(
            "Campus Report",
            f"""
Total Bookings: {report[0]}

Most Used Resource:
{report[1]}

Average Duration:
{report[2]}
"""
        )

    def show_cross_report(self):

        data = cross_campus_report()

        output = ""

        for campus in data:
            output += f"{campus[0]} : {campus[1]} bookings\n"

        if output == "":
            output = "No booking data available."

        messagebox.showinfo(
            "Cross Campus Report",
            output
        )


# ==========================
# BOOKING WINDOW
# ==========================

class BookingWindow(Toplevel):

    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id

        self.title("Resource Booking")
        self.geometry("400x350")

        Label(self, text="Resource ID").pack()

        self.resource = Entry(self)
        self.resource.pack()

        Label(self, text="Booking Date (YYYY-MM-DD)").pack()

        self.date = Entry(self)
        self.date.pack()

        Label(self, text="Start Time").pack()

        self.time = Entry(self)
        self.time.pack()

        Label(self, text="Duration (Hours)").pack()

        self.duration = Entry(self)
        self.duration.pack()

        Button(
            self,
            text="Book Resource",
            command=self.save_booking
        ).pack(pady=10)

    def save_booking(self):

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        resource = self.resource.get()
        date = self.date.get()
        time = self.time.get()
        duration = self.duration.get()

        cursor.execute(
            """
            SELECT *
            FROM bookings
            WHERE resource_id = ?
            AND booking_date = ?
            AND start_time = ?
            """,
            (
                resource,
                date,
                time
            )
        )

        existing = cursor.fetchone()

        if existing:

            messagebox.showerror(
                "Error",
                "Resource already booked at this time."
            )

            conn.close()
            return

        cursor.execute(
            """
            INSERT INTO bookings
            (
                user_id,
                resource_id,
                booking_date,
                start_time,
                duration
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                self.user_id,
                resource,
                date,
                time,
                duration
            )
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Booking Saved Successfully"
        )

        self.destroy()