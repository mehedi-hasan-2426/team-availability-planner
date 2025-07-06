import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.views.main_window import MonthlyPlannerApp
from src.models.database import DatabaseManager

def main():
    try:
        DatabaseManager.initialize_database()
        
        app = QApplication(sys.argv)
        app.setApplicationName("Team Availability")
        app.setApplicationVersion("1.0")
        
        window = MonthlyPlannerApp()
        window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
