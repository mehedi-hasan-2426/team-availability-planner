import calendar
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QInputDialog, QMessageBox, QLineEdit)
from PyQt6.QtCore import Qt
from src.models.database import DatabaseManager

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee")
        self.setModal(True)
        self.resize(300, 150)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Employee Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Select Location:"))
        self.location_combo = QComboBox()
        self.location_combo.addItems(["Essen", "UK", "USA"])
        layout.addWidget(self.location_combo)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        self.name_input.returnPressed.connect(self.accept)

    def get_employee_info(self):
        return self.name_input.text().strip(), self.location_combo.currentText()

    @staticmethod
    def show_dialog(parent):
        """Show add employee dialog"""
        dialog = AddEmployeeDialog(parent)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, location = dialog.get_employee_info()
            if name and location:
                if DatabaseManager.add_employee(name, location):
                    parent.load_data()
                    QMessageBox.information(parent, "Success", f"Employee {name} added successfully!")
                else:
                    QMessageBox.critical(parent, "Error", "Failed to add employee. Employee might already exist.")
            else:
                QMessageBox.warning(parent, "Warning", "Please enter a valid name.")

    @staticmethod
    def show_remove_dialog(parent):
        """Show remove employee dialog"""
        employees = DatabaseManager.get_employees()
        if not employees:
            QMessageBox.information(parent, "No Employees", "There are no employees to remove.")
            return
        
        employee, ok = QInputDialog.getItem(parent, "Remove Employee", 
                                          "Select an employee to remove:", 
                                          employees, 0, False)
        if ok and employee:
            reply = QMessageBox.question(parent, "Confirm Removal", 
                                       f"Are you sure you want to remove {employee}?\\n"
                                       "This will delete all associated data.",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                if DatabaseManager.remove_employee(employee):
                    parent.load_data()
                    QMessageBox.information(parent, "Success", 
                                          f"Employee {employee} removed successfully!")
                else:
                    QMessageBox.critical(parent, "Error", "Failed to remove employee")

    @staticmethod
    def update_view(table_widget, location, current_month):
        """Update table view with employees and calendar data"""
        try:
            employees = DatabaseManager.get_employees_by_location(location)
            days_in_month = calendar.monthrange(current_month.year, current_month.month)[1]
            
            # Set table dimensions
            table_widget.setColumnCount(days_in_month + 1)
            table_widget.setRowCount(len(employees) + 1)
            
            # Populate table using DatabaseManager
            DatabaseManager.populate_table(table_widget, employees, current_month, days_in_month)
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while updating view: {str(e)}")
            print(f"Error in update_view: {e}")
