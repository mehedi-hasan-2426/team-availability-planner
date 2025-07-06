import os
import calendar
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QScrollArea, QSizePolicy, QPushButton, QTableWidget, 
                           QTableWidgetItem, QComboBox, QMessageBox, QColorDialog,
                           QInputDialog)
from PyQt6.QtGui import QColor, QIcon

from src.views.legend import LegendItem
from src.views.dialogs import AddEmployeeDialog
from src.models.database import DatabaseManager

class MonthlyPlannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_location = "All"
        self.current_month = datetime.now().replace(day=1)
        self.employees = []
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Team Availability Planner")
        self.setGeometry(100, 100, 1600, 800)
        
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "TA_Logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        self.setup_legend_panel(main_layout)
        self.setup_planner_panel(main_layout)
        
        self.setCentralWidget(main_widget)

    def setup_legend_panel(self, main_layout):
        legend_widget = QWidget()
        legend_widget.setMaximumWidth(300)
        legend_layout = QVBoxLayout(legend_widget)
        
        LegendItem.setup_legend(legend_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(legend_widget)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        main_layout.addWidget(scroll_area, 1)

    def setup_planner_panel(self, main_layout):
        planner_layout = QVBoxLayout()
        
        self.setup_date_controls(planner_layout)
        self.setup_table(planner_layout)
        self.setup_control_buttons(planner_layout)
        
        main_layout.addLayout(planner_layout, 4)

    def setup_date_controls(self, layout):
        date_controls = QHBoxLayout()
        
        current_year = datetime.now().year
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(year) for year in range(current_year - 5, current_year + 6)])
        self.year_combo.setCurrentText(str(current_year))
        self.year_combo.currentTextChanged.connect(self.date_changed)
        
        self.month_combo = QComboBox()
        self.month_combo.addItems(calendar.month_name[1:])
        self.month_combo.setCurrentText(calendar.month_name[datetime.now().month])
        self.month_combo.currentTextChanged.connect(self.date_changed)
        
        date_controls.addWidget(QWidget())
        date_controls.addWidget(self.year_combo)
        date_controls.addWidget(self.month_combo)
        date_controls.addWidget(QWidget())
        
        layout.addLayout(date_controls)

    def setup_table(self, layout):
        """Setup the main data table"""
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)
        
        # Connect cell change signal
        self.table_widget.cellChanged.connect(self.on_cell_changed)
        
        layout.addWidget(self.table_widget)

    def setup_control_buttons(self, layout):
        """Setup control buttons at the bottom"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Location filter buttons
        locations = ["All", "Essen", "UK", "USA"]
        for location in locations:
            btn = QPushButton(location)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, loc=location: self.update_view(loc))
            if location == "All":
                btn.setChecked(True)
            button_layout.addWidget(btn)
        
        button_layout.addStretch()
        
        # Action buttons
        color_day_btn = QPushButton("Color Day")
        color_day_btn.clicked.connect(self.color_specific_day)
        button_layout.addWidget(color_day_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)
        button_layout.addWidget(save_btn)
        
        add_employee_btn = QPushButton("Add Employee")
        add_employee_btn.clicked.connect(self.show_add_employee_dialog)
        button_layout.addWidget(add_employee_btn)
        
        remove_employee_btn = QPushButton("Remove Employee")
        remove_employee_btn.clicked.connect(self.show_remove_employee_dialog)
        button_layout.addWidget(remove_employee_btn)
        
        layout.addLayout(button_layout)

    def date_changed(self):
        """Handle date change event"""
        try:
            year = int(self.year_combo.currentText())
            month = list(calendar.month_name).index(self.month_combo.currentText())
            self.current_month = datetime(year, month, 1)
            self.update_current_month()
        except (ValueError, IndexError):
            pass

    def update_current_month(self):
        """Update the display for the current month"""
        AddEmployeeDialog.update_view(self.table_widget, self.current_location, self.current_month)
        self.apply_saved_colors()

    def load_data(self):
        """Load data for the current view"""
        self.employees = DatabaseManager.get_employees_by_location(self.current_location)
        self.update_current_month()

    def update_view(self, location):
        """Update the table view based on selected location"""
        # Update button states
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["All", "Essen", "UK", "USA"]:
                btn.setChecked(btn.text() == location)
        
        self.current_location = location
        self.employees = DatabaseManager.get_employees_by_location(location)
        self.update_current_month()

    def color_specific_day(self):
        """Color a specific day column in the table and save the color"""
        days_in_month = calendar.monthrange(self.current_month.year, self.current_month.month)[1]
        days = [str(i) for i in range(1, days_in_month + 1)]
        day, ok = QInputDialog.getItem(self, "Select Day", 
                                      "Choose a day to color:", 
                                      days, 0, False)
        
        if not ok:
            return
            
        color = QColorDialog.getColor()
        if not color.isValid():
            return
        
        color_hex = color.name()
        day_int = int(day)
        
        # Color the column
        for col in range(1, self.table_widget.columnCount()):
            header_item = self.table_widget.item(0, col)
            if header_item and header_item.text().startswith(f"{day_int:02d}"):
                header_item.setBackground(color)
                for row in range(1, self.table_widget.rowCount()):
                    cell = self.table_widget.item(row, col)
                    if cell:
                        cell.setBackground(color)
                
                # Save color to database
                date = self.current_month.replace(day=day_int)
                date_str = date.strftime("%Y.%m.%d")
                DatabaseManager.save_column_color(date_str, color_hex)
                break

    def apply_saved_colors(self):
        """Apply saved colors to columns"""
        saved_colors = DatabaseManager.get_column_colors()
        
        for date_str, color_hex in saved_colors:
            try:
                date = datetime.strptime(date_str, "%Y.%m.%d")
                if date.year == self.current_month.year and date.month == self.current_month.month:
                    day = date.day
                    for col in range(1, self.table_widget.columnCount()):
                        header_item = self.table_widget.item(0, col)
                        if header_item and header_item.text().startswith(f"{day:02d}"):
                            color = QColor(color_hex)
                            header_item.setBackground(color)
                            for row in range(1, self.table_widget.rowCount()):
                                cell = self.table_widget.item(row, col)
                                if cell:
                                    cell.setBackground(color)
                            break
            except (ValueError, AttributeError):
                continue

    def on_cell_changed(self, row, column):
        """Handle cell content changes"""
        if row == 0 or column == 0:  # Skip header row and name column
            return
        
        # Auto-save is handled when save button is clicked
        pass

    def save_data(self):
        """Save all data to database"""
        try:
            entries = []
            days_in_month = calendar.monthrange(self.current_month.year, self.current_month.month)[1]
            
            # Clear existing entries for this month and employees
            if self.employees:
                employee_ids = [emp_id for emp_id, _ in self.employees]
                start_date = self.current_month.strftime("%Y-%m-01")
                end_date = self.current_month.strftime(f"%Y-%m-{days_in_month:02d}")
                DatabaseManager.clear_month_entries(start_date, end_date, employee_ids)
            
            # Collect new entries
            for row in range(1, self.table_widget.rowCount()):
                if row - 1 < len(self.employees):
                    emp_id, emp_name = self.employees[row - 1]
                    
                    for col in range(1, min(self.table_widget.columnCount(), days_in_month + 1)):
                        item = self.table_widget.item(row, col)
                        if item and item.text().strip():
                            date = self.current_month.replace(day=col)
                            date_str = date.strftime("%Y-%m-%d")
                            entries.append((date_str, emp_id, item.text().strip()))
            
            # Save to database
            if DatabaseManager.save_planner_entries(entries):
                QMessageBox.information(self, "Success", "Data saved successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save data")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving data: {str(e)}")

    def show_add_employee_dialog(self):
        """Show add employee dialog"""
        AddEmployeeDialog.show_dialog(self)

    def show_remove_employee_dialog(self):
        """Show remove employee dialog"""
        AddEmployeeDialog.show_remove_dialog(self)
