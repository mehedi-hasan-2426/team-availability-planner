import sqlite3
import calendar
import os
from datetime import datetime
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

class DatabaseManager:
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "team_availability.db")

    @staticmethod
    def initialize_database():
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EmployeeLocations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    location TEXT NOT NULL,
                    FOREIGN KEY (employee_id) REFERENCES Employees (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PlannerEntries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    date TEXT NOT NULL,
                    note TEXT,
                    FOREIGN KEY (employee_id) REFERENCES Employees (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ColumnColors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    color TEXT NOT NULL
                )
            """)
            
            cursor.execute("SELECT COUNT(*) FROM Employees")
            if cursor.fetchone()[0] == 0:
                default_employees = [
                    ("John Doe", "Essen"),
                    ("Jane Smith", "UK"),
                    ("Bob Johnson", "USA"),
                    ("Alice Brown", "Essen"),
                    ("Charlie Wilson", "UK")
                ]
                
                for name, location in default_employees:
                    cursor.execute("INSERT INTO Employees (name) VALUES (?)", (name,))
                    employee_id = cursor.lastrowid
                    cursor.execute("INSERT INTO EmployeeLocations (employee_id, location) VALUES (?, ?)", 
                                 (employee_id, location))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_employees_by_location(location):
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            if location == "All":
                cursor.execute("SELECT id, name FROM Employees ORDER BY name")
            else:
                cursor.execute("""
                    SELECT e.id, e.name 
                    FROM Employees e
                    INNER JOIN EmployeeLocations el ON e.id = el.employee_id
                    WHERE el.location = ?
                    ORDER BY e.name
                """, (location,))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def add_employee(name, location):
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Employees (name) VALUES (?)", (name,))
            employee_id = cursor.lastrowid
            cursor.execute("INSERT INTO EmployeeLocations (employee_id, location) VALUES (?, ?)", 
                         (employee_id, location))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding employee: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def remove_employee(employee_name):
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM Employees WHERE name = ?", (employee_name,))
            result = cursor.fetchone()
            if not result:
                return False
            
            employee_id = result[0]
            cursor.execute("DELETE FROM PlannerEntries WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM EmployeeLocations WHERE employee_id = ?", (employee_id,))
            cursor.execute("DELETE FROM Employees WHERE id = ?", (employee_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error removing employee: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_employees():
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT name FROM Employees ORDER BY name")
            employees = [row[0] for row in cursor.fetchall()]
            return employees
        finally:
            conn.close()

    @staticmethod
    def save_column_color(date_str, color_hex):
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO ColumnColors (date, color) 
                VALUES (?, ?)
            """, (date_str, color_hex))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving column color: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_column_colors():
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT date, color FROM ColumnColors")
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def clear_month_entries(start_date, end_date, employee_ids):
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            if not employee_ids:
                return True
            
            placeholders = ','.join('?' * len(employee_ids))
            cursor.execute(f"""
                DELETE FROM PlannerEntries 
                WHERE date BETWEEN ? AND ?
                AND employee_id IN ({placeholders})
            """, (start_date, end_date, *employee_ids))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing month entries: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def save_planner_entries(entries):
        if not entries:
            return True
            
        valid_entries = [(date, emp_id, note) for date, emp_id, note in entries 
                        if note and note.strip()]
        
        if not valid_entries:
            return True
            
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.executemany("""
                INSERT INTO PlannerEntries (date, employee_id, note) 
                VALUES (?, ?, ?)
            """, valid_entries)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving planner entries: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_planner_entries(start_date, end_date, employee_ids):
        if not employee_ids:
            return []
            
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        try:
            placeholders = ','.join('?' * len(employee_ids))
            cursor.execute(f"""
                SELECT date, employee_id, note 
                FROM PlannerEntries 
                WHERE date BETWEEN ? AND ? 
                AND employee_id IN ({placeholders})
            """, (start_date, end_date, *employee_ids))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def populate_table(table_widget, employees, current_month, days_in_month):
        try:
            month_name = calendar.month_name[current_month.month]
            table_widget.setItem(0, 0, QTableWidgetItem(f"{month_name} {current_month.year}"))
            
            for day in range(1, days_in_month + 1):
                date = current_month.replace(day=day)
                day_name = date.strftime("%a")
                header_text = f"{day:02d} {day_name}"
                
                item = QTableWidgetItem(header_text)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                
                if date.weekday() >= 5:
                    item.setBackground(QColor(230, 230, 230))
                
                font = QFont()
                font.setBold(True)
                item.setFont(font)
                table_widget.setItem(0, day, item)
            
            for row, (emp_id, emp_name) in enumerate(employees, 1):
                name_item = QTableWidgetItem(emp_name)
                name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                font = QFont()
                font.setBold(True)
                name_item.setFont(font)
                table_widget.setItem(row, 0, name_item)
                
                for day in range(1, days_in_month + 1):
                    date = current_month.replace(day=day)
                    cell_item = QTableWidgetItem("")
                    
                    if date.weekday() >= 5:
                        cell_item.setBackground(QColor(240, 240, 240))
                    
                    table_widget.setItem(row, day, cell_item)
            
            if employees:
                employee_ids = [emp_id for emp_id, _ in employees]
                start_date = current_month.strftime("%Y-%m-01")
                end_date = current_month.strftime(f"%Y-%m-{days_in_month:02d}")
                
                entries = DatabaseManager.get_planner_entries(start_date, end_date, employee_ids)
                
                for date_str, emp_id, note in entries:
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d")
                        day = date.day
                        
                        for row, (e_id, _) in enumerate(employees, 1):
                            if e_id == emp_id:
                                item = table_widget.item(row, day)
                                if item:
                                    item.setText(note)
                                break
                    except (ValueError, AttributeError):
                        continue
            
            table_widget.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error populating table: {e}")
