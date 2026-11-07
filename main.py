import sqlite3
from datetime import date

DB_NAME = "employees.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_table():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL CHECK (salary >= 0),
                hire_date TEXT NOT NULL
            )
            """
        )


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number.")


def employee_exists(emp_id):
    with connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM employees WHERE id = ?", (emp_id,)
        ).fetchone()
    return row is not None


def print_employees(rows):
    if not rows:
        print("No employees found.")
        return
    print(
        f"\n{'ID':<6}{'Name':<18}{'Department':<14}"
        f"{'Position':<16}{'Salary':<12}{'Hired':<12}"
    )
    print("-" * 78)
    for emp_id, name, dept, pos, salary, hired in rows:
        print(
            f"{emp_id:<6}{name:<18}{dept:<14}"
            f"{pos:<16}{salary:<12.2f}{hired:<12}"
        )


def add_employee():
    emp_id = read_int("Employee ID: ")
    if employee_exists(emp_id):
        print("An employee with this ID already exists.")
        return
    name = input("Name: ").strip()
    dept = input("Department: ").strip()
    position = input("Position: ").strip()
    salary = read_float("Salary: ")
    if not name or not dept or not position or salary < 0:
        print("Invalid input. Nothing was saved.")
        return
    with connect() as conn:
        conn.execute(
            "INSERT INTO employees (id, name, department, position, salary, hire_date) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (emp_id, name, dept, position, salary, date.today().isoformat()),
        )
    print("Employee added successfully.")


def list_employees():
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, department, position, salary, hire_date "
            "FROM employees ORDER BY id"
        ).fetchall()
    print_employees(rows)


def search_employees():
    keyword = input("Search by name or department: ").strip()
    pattern = f"%{keyword}%"
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, department, position, salary, hire_date "
            "FROM employees WHERE name LIKE ? OR department LIKE ? ORDER BY id",
            (pattern, pattern),
        ).fetchall()
    print_employees(rows)


def update_employee():
    emp_id = read_int("Employee ID to update: ")
    if not employee_exists(emp_id):
        print("Employee not found.")
        return
    dept = input("New department: ").strip()
    position = input("New position: ").strip()
    salary = read_float("New salary: ")
    if not dept or not position or salary < 0:
        print("Invalid input. Nothing was changed.")
        return
    with connect() as conn:
        conn.execute(
            "UPDATE employees SET department = ?, position = ?, salary = ? "
            "WHERE id = ?",
            (dept, position, salary, emp_id),
        )
    print("Employee updated successfully.")


def delete_employee():
    emp_id = read_int("Employee ID to delete: ")
    if not employee_exists(emp_id):
        print("Employee not found.")
        return
    with connect() as conn:
        conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    print("Employee deleted successfully.")


def department_report():
    with connect() as conn:
        rows = conn.execute(
            "SELECT department, COUNT(*), AVG(salary), SUM(salary) "
            "FROM employees GROUP BY department ORDER BY department"
        ).fetchall()
    if not rows:
        print("No employees found.")
        return
    print(f"\n{'Department':<16}{'Count':<8}{'Avg Salary':<14}{'Total Salary':<14}")
    print("-" * 52)
    for dept, count, avg, total in rows:
        print(f"{dept:<16}{count:<8}{avg:<14.2f}{total:<14.2f}")


def highest_paid():
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, department, position, salary, hire_date "
            "FROM employees ORDER BY salary DESC LIMIT 3"
        ).fetchall()
    print("\nTop 3 highest paid employees:")
    print_employees(rows)


def main():
    create_table()
    actions = {
        "1": add_employee,
        "2": list_employees,
        "3": search_employees,
        "4": update_employee,
        "5": delete_employee,
        "6": department_report,
        "7": highest_paid,
    }
    while True:
        print("\n=== Employee Management System ===")
        print("1. Add Employee")
        print("2. List Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Department Report")
        print("7. Top 3 Highest Paid")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()