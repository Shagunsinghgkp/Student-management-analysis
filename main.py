import tkinter as tk
import sqlite3
import csv
from tkinter import messagebox
from tkinter import ttk
# Database create
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT,
    semester TEXT
)
""")

conn.commit()
try:
    cursor.execute("ALTER TABLE students ADD COLUMN marks INTEGER")
    conn.commit()
except sqlite3.OperationalError:
    pass
try:
    cursor.execute("ALTER TABLE students ADD COLUMN attendance REAL")
    conn.commit()
except sqlite3.OperationalError:
    pass

# Add student function
def add_student():
    student_id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    semester = semester_entry.get()
    marks = marks_entry.get()
    attendance = attendance_entry.get()

    if student_id == "" or name == "" or age == "" or course == "" or semester == "" or marks == "" or attendance == "":
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_id, name, age, course, semester, marks, attendance)
        )
        conn.commit()

        messagebox.showinfo("Success", "Student added successfully!")

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        semester_entry.delete(0, tk.END)
        marks_entry.delete(0, tk.END)
        attendance_entry.delete(0, tk.END)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists.")
# View students function
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("Students", "No students found.")
        return

    result = ""
    for student in students:
        result += f"ID: {student[0]}\n"
        result += f"Name: {student[1]}\n"
        result += f"Age: {student[2]}\n"
        result += f"Course: {student[3]}\n"
        result += f"Semester: {student[4]}\n"
        result += f"Marks: {student[5]}\n"
        result += f"Attendance: {student[6]}%\n"
        result += "-" * 30 + "\n"

    messagebox.showinfo("All Students", result)
def export_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("Export", "No students found.")
        return

    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Name",
            "Age",
            "Course",
            "Semester",
            "Marks",
            "Attendance"
        ])

        writer.writerows(students)

    messagebox.showinfo(
        "Export Successful",
        "Student data exported to students.csv"
    )
def search_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        result = f"ID: {student[0]}\n"
        result += f"Name: {student[1]}\n"
        result += f"Age: {student[2]}\n"
        result += f"Course: {student[3]}\n"
        result += f"Semester: {student[4]}"
        result += f"Marks: {student[5]}\n"
        result += f"Attendance: {student[6]}%\n"

        messagebox.showinfo("Student Found", result)
    else:
        messagebox.showerror("Error", "Student ID not found.")
def delete_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student deleted successfully!")
        id_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Student ID not found.")


def update_student():
    student_id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    semester = semester_entry.get()
    attendance = attendance_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        """
        UPDATE students
        SET name = ?, age = ?, course = ?, semester = ?, attendance = ?
        WHERE student_id = ?
        """,
        (name, age, course, semester, attendance, student_id)
    )

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Student updated successfully!")
    else:
        messagebox.showerror("Error", "Student ID not found.")
def search_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        result = f"ID: {student[0]}\n"
        result += f"Name: {student[1]}\n"
        result += f"Age: {student[2]}\n"
        result += f"Course: {student[3]}\n"
        result += f"Semester: {student[4]}\n"
        result += f"Marks: {student[5]}\n"
        result += f"Attendance: {student[6]}%\n"

        messagebox.showinfo("Student Found", result)
    else:
        messagebox.showerror("Error", "Student not found.")       
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)
def total_students():
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    messagebox.showinfo(
        "Total Students",
        f"Total Students: {count}"
    )
def pass_fail_status():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        "SELECT marks FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        messagebox.showerror("Error", "Student not found.")
        return

    marks = student[0]

    if marks is None:
        messagebox.showwarning("Warning", "Marks not available.")
        return

    if marks >= 21:
        status = "PASS"
    else:
        status = "FAIL"

    messagebox.showinfo(
        "Result",
        f"Student ID: {student_id}\nMarks: {marks}\nStatus: {status}"
    )
def view_students_table():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("Students", "No students found.")
        return

    table_window = tk.Toplevel(root)
    table_window.title("Student Records")
    table_window.geometry("900x400")

    columns = (
        "ID",
        "Name",
        "Age",
        "Course",
        "Semester",
        "Marks",
        "Attendance"
    )

    tree = ttk.Treeview(
        table_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=120)

    for student in students:
        tree.insert("", tk.END, values=student)

    tree.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        table_window,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
def attendance_status():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Please enter Student ID.")
        return

    cursor.execute(
        "SELECT attendance FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        messagebox.showerror("Error", "Student not found.")
        return

    attendance = student[0]

    if attendance is None:
        messagebox.showwarning("Warning", "Attendance not available.")
        return

    if float(attendance) >= 75:
        status = "GOOD"
    else:
        status = "LOW"

    messagebox.showinfo(
        "Attendance Status",
        f"Student ID: {student_id}\n"
        f"Attendance: {attendance}%\n"
        f"Status: {status}"
    )
def highest_lowest_marks():
    cursor.execute("""
        SELECT name, marks
        FROM students
        WHERE marks IS NOT NULL
        ORDER BY marks DESC
    """)

    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("Marks", "No marks available.")
        return

    highest_name = students[0][0]
    highest_marks = students[0][1]

    lowest_name = students[-1][0]
    lowest_marks = students[-1][1]

    messagebox.showinfo(
        "Highest & Lowest Marks",
        f"Highest Marks:\n{highest_name} - {highest_marks}\n\n"
        f"Lowest Marks:\n{lowest_name} - {lowest_marks}"
    )
def average_marks():
    cursor.execute("SELECT AVG(marks) FROM students")
    average = cursor.fetchone()[0]

    if average is None:
        messagebox.showinfo("Average Marks", "No marks available.")
    else:
        messagebox.showinfo(
            "Average Marks",
            f"Average Marks: {average:.2f}"
        )
def exit_app():
    root.destroy()
# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x800")
# Scrollable Frame
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw",
    width=680
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
root.resizable(True, True)

heading = tk.Label(
    scrollable_frame,
    text="Student Management System",
    font=("Arial", 20, "bold")
)
heading.pack(pady=15)

# Student ID
tk.Label(scrollable_frame, text="Student ID:", font=("Arial", 12)).pack()
id_entry = tk.Entry(scrollable_frame, width=40)
id_entry.pack(pady=5)

# Name
tk.Label(scrollable_frame, text="Name:", font=("Arial", 12)).pack()
name_entry = tk.Entry(scrollable_frame, width=40)
name_entry.pack(pady=5)

# Age
tk.Label(scrollable_frame, text="Age:", font=("Arial", 12)).pack()
age_entry = tk.Entry(scrollable_frame, width=40)
age_entry.pack(pady=5)

# Course
tk.Label(scrollable_frame, text="Course:", font=("Arial", 12)).pack()
course_entry = tk.Entry(scrollable_frame, width=40)
course_entry.pack(pady=5)

# Semester
tk.Label(scrollable_frame, text="Semester:", font=("Arial", 12)).pack()
semester_entry = tk.Entry(scrollable_frame, width=40)
semester_entry.pack(pady=5)
marks_label = tk.Label(scrollable_frame, text="Marks:", font=("Arial", 12))
marks_label.pack()

marks_entry = tk.Entry(scrollable_frame, width=40)
marks_entry.pack(pady=5)
attendance_label = tk.Label(scrollable_frame, text="Attendance (%):", font=("Arial", 12))
attendance_label.pack()

attendance_entry = tk.Entry(scrollable_frame, width=40)
attendance_entry.pack(pady=5)
# Add button
add_button = tk.Button(
    scrollable_frame,
    text="Add Student",
    font=("Arial", 12, "bold"),
    command=add_student
)
add_button.pack(pady=20)
view_button = tk.Button(
    scrollable_frame,
    text="View Students",
    font=("Arial", 12, "bold"),
    command=view_students
)
view_button.pack(pady=5)
delete_button = tk.Button(
    scrollable_frame,
    text="Delete Student",
    font=("Arial", 12, "bold"),
    command=delete_student
)
delete_button.pack(pady=5)
update_button = tk.Button(
    scrollable_frame,
    text="Update Student",
    font=("Arial", 12, "bold"),
    command=update_student
)
update_button.pack(pady=5)
search_button = tk.Button(
    scrollable_frame,
    text="Search Student",
    font=("Arial", 12, "bold"),
    command=search_student
)
search_button.pack(pady=5)
clear_button = tk.Button(
    scrollable_frame,
    text="Clear Fields",
    font=("Arial", 12, "bold"),
    command=clear_fields
)
clear_button.pack(pady=5)
count_button = tk.Button(
    scrollable_frame,
    text="Total Students",
    font=("Arial", 12, "bold"),
    command=total_students
)
count_button.pack(pady=5)
average_button = tk.Button(
    scrollable_frame,
    text="Average Marks",
    font=("Arial", 12, "bold"),
    command=average_marks
)
average_button.pack(pady=5)
exit_button = tk.Button(
    scrollable_frame,
    text="Exit",
    font=("Arial", 12, "bold"),
    command=exit_app
)
status_button = tk.Button(
    scrollable_frame,
    text="Pass/Fail Status",
    font=("Arial", 12, "bold"),
    command=pass_fail_status
)
status_button.pack(pady=5)
exit_button.pack(pady=5)
attendance_status_button = tk.Button(
    scrollable_frame,
    text="Attendance Status",
    font=("Arial", 12, "bold"),
    command=attendance_status
)
attendance_status_button.pack(pady=5)
highest_lowest_button = tk.Button(
    scrollable_frame,
    text="Highest & Lowest Marks",
    font=("Arial", 12, "bold"),
    command=highest_lowest_marks
)
highest_lowest_button.pack(pady=5)
export_button = tk.Button(
    scrollable_frame,
    text="Export Students",
    font=("Arial", 12, "bold"),
    command=export_students
)
export_button.pack(pady=5)
table_button = tk.Button(
    scrollable_frame,
    text="View Students Table",
    font=("Arial", 12, "bold"),
    command=view_students_table
)
table_button.pack(pady=5)
root.mainloop()