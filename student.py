import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('student.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL
)''')

conn.commit()

root = tk.Tk()
root.title("School Management System")
root.geometry("500x500")
root.configure(background='lightblue')

course = ["Computer Science", "Information Technology", "Engineering", "Mathematics"]

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def login_screen():
    clear_frame()
    label = tk.Label(root, text="Login Account", font=("bold", 30), bg=root["bg"])
    label.pack(pady=10)

    tk.Label(root, text="Username:", font=("Arial", 16), bg=root["bg"]).pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=8)

    tk.Label(root, text="Password:", font=("Arial", 16), bg=root["bg"]).pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=8)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Oops", "Please fill in all fields!")
            return

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successfully", "Welcome to School Management")
            main_menu()
        else:
            messagebox.showerror("Oops", "Invalid username or password")

    def go_to_register():
        register_screen()

    tk.Button(root, text="Login", command=login, width=20).pack(pady=10)
    tk.Button(root, text="Register", command=go_to_register, width=20).pack(pady=5)

def register_screen():
    clear_frame()
    label = tk.Label(root, text="Register Account", font=("bold", 30), bg=root["bg"])
    label.pack(pady=10)

    tk.Label(root, text="Username:", font=("Arial", 16), bg=root["bg"]).pack()
    username_entry = tk.Entry(root)
    username_entry.pack(pady=8)

    tk.Label(root, text="Password:", font=("Arial", 16), bg=root["bg"]).pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=8)

    tk.Label(root, text="Confirm Password:", font=("Arial", 16), bg=root["bg"]).pack()
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=8)

    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Oops", "Please fill in all fields")
            return
        if password != confirm_password:
            messagebox.showerror("Oops", "Passwords do not match")
            return

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Oops", "Username already exists")
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration", "Register successfully!")
        login_screen()

    tk.Button(root, text="Register", command=register, width=20).pack(pady=10)
    tk.Button(root, text="Back to Login", command=login_screen, width=20).pack(pady=5)

def register_students():
    clear_frame()
    label = tk.Label(root, text="Register Students", font=("bold", 30), bg=root["bg"])
    label.pack(pady=10)

    def create_student_entry_form():
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:", width=20, anchor="w").grid(row=0, column=0)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=0, column=1)

        tk.Label(frame, text="Age:", width=20, anchor="w").grid(row=1, column=0)
        age_entry = tk.Entry(frame)
        age_entry.grid(row=1, column=1)

        tk.Label(frame, text="Address:", width=20, anchor="w").grid(row=2, column=0)
        address_entry = tk.Entry(frame)
        address_entry.grid(row=2, column=1)

        tk.Label(frame, text="Email:", width=20, anchor="w").grid(row=3, column=0)
        email_entry = tk.Entry(frame)
        email_entry.grid(row=3, column=1)

        tk.Label(frame, text="Course:", width=20, anchor="w").grid(row=4, column=0)
        course_choice = tk.StringVar()
        course_menu = tk.OptionMenu(frame, course_choice, *course)
        course_menu.grid(row=4, column=1)

        return (name_entry, age_entry, address_entry, email_entry, course_choice)

    student_entries = []
    def add_new_entry_form():
        new_entry = create_student_entry_form()
        student_entries.append(new_entry)

    def save_students():
        try:
            for entry in student_entries:
                name, age, address, email, course_choice = entry
                if not (name.get() and age.get() and address.get() and email.get() and course_choice.get()):
                    messagebox.showerror("Missing Data", "Please fill in all fields for each student")
                    return

                cursor.execute("INSERT INTO students (name, age, address, email, course) VALUES (?, ?, ?, ?, ?)",
                               (name.get(), age.get(), address.get(), email.get(), course_choice.get()))
            conn.commit()
            messagebox.showinfo("Success", "Students registered successfully!")
            main_menu()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(root, text="Add Another Student", command=add_new_entry_form).pack(pady=5)
    tk.Button(root, text="Register All Students", command=save_students).pack(pady=10)
    tk.Button(root, text="Back to Main Menu", command=main_menu).pack(pady=10)
    add_new_entry_form()

def delete_student(student_id):
    try:
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student record deleted successfully!")
        show_database()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def show_database():
    clear_frame()
    label = tk.Label(root, text="Database", font=("bold", 30), bg=root["bg"])
    label.pack(pady=10)

    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if not students:
            tk.Label(root, text="No student records found.", font=("Arial", 14), bg=root["bg"]).pack(pady=5)
        else:
            for student in students:
                student_id = student[0]
                tk.Label(root, text=f"Name: {student[1]}", font=("Arial", 12), bg=root["bg"]).pack(anchor="w")
                tk.Label(root, text=f"Age: {student[2]}", font=("Arial", 12), bg=root["bg"]).pack(anchor="w")
                tk.Label(root, text=f"Address: {student[3]}", font=("Arial", 12), bg=root["bg"]).pack(anchor="w")
                tk.Label(root, text=f"Email: {student[4]}", font=("Arial", 12), bg=root["bg"]).pack(anchor="w")
                tk.Label(root, text=f"Course: {student[5]}", font=("Arial", 12), bg=root["bg"]).pack(anchor="w")

                def confirm_delete():
                    if messagebox.askyesno("Confirmation", "Are you sure you want to delete this student?"):
                        delete_student(student_id)

                delete_button = tk.Button(root, text="Delete", command=confirm_delete, width=10, bg='red')
                delete_button.pack(pady=5)

                tk.Label(root, text="-" * 100, bg=root["bg"]).pack(anchor="w")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    tk.Button(root, text="Back to Main Menu", command=main_menu).pack(pady=20)

def main_menu():
    clear_frame()
    label = tk.Label(root, text="Main Menu", font=("bold", 30), bg=root["bg"])
    label.pack(pady=10)

    tk.Button(root, text="Register Students", command=register_students, width=20).pack(pady=5)
    tk.Button(root, text="Show Database", command=show_database, width=20).pack(pady=5)
    tk.Button(root, text="Logout", command=login_screen, width=20).pack(pady=5)

login_screen()

root.mainloop()
conn.close()