# Team Availability Planner

A desktop application for planning and tracking team availability, built with Python and PyQt6.

## Features

- 📅 Monthly calendar view for easy planning
- 👥 Employee management with location assignments
- 🌍 Location filtering (All, Essen, UK, USA)
- 🎨 Color coding for specific days
- 💾 SQLite database with automatic creation
- 🔄 Auto-save functionality
- 📊 Clear availability legend

## Quick Start

### Windows (Recommended)
1. Double-click `start_app.bat` to automatically set up and run the application

### Manual Setup
1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
TAA Classes/
├── src/
│   ├── models/
│   │   └── database.py
│   ├── views/
│   │   ├── main_window.py
│   │   ├── dialogs.py
│   │   └── legend.py
│   └── main.py
├── main.py
├── run.py
├── requirements.txt
└── start_app.bat
```

## Usage

1. **View Planning**: Select month/year and location filter
2. **Add Employees**: Use the "Add Employee" button
3. **Plan Availability**: Click on calendar cells to add notes
4. **Save Changes**: Click "Save Month" to persist data
5. **Color Days**: Use "Color Day" to highlight specific dates

## Requirements

- Python 3.8+
- PyQt6
- SQLite3 (included with Python)

## License

MIT License

## Availability Legend

The legend shows different types of availability and their meanings:

- **Business Trip (BT)** - Employee on business travel
- **Parental Leave (PL)** - Employee on parental leave
- **Compassionate Leave (CL)** - Employee on compassionate leave
- **Home Office (HO)** - Employee working from home
- **Vacation (V)** - Employee on vacation
- **Training (T)** - Employee in training
- **Bank Holidays** - Various regional bank holidays (color-coded)
- **School Holidays** - Regional school holidays (color-coded)
- **Team Events** - Team meetings or events
- **Planned Go Live** - Project go-live dates

## Database

The application uses SQLite for local data storage with the following tables:

- **Employees**: Employee information
- **EmployeeLocations**: Employee location assignments
- **PlannerEntries**: Availability entries
- **ColumnColors**: Saved day colors

The database file (`team_availability.db`) is created automatically in the application directory.

## Troubleshooting

### Import Errors
If you get import errors, make sure PyQt6 is installed:
```bash
pip install PyQt6
```

### Database Issues
If you encounter database issues, delete `team_availability.db` to reset the database.

### Virtual Environment
For a clean setup, use a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py
```

## Requirements

- Python 3.8+
- PyQt6 6.5.0+
- SQLite (included with Python)

## Comparison with Original C# Version

This Python version replicates the core functionality of the original C# Windows Forms application:

✅ **Implemented Features:**
- Monthly calendar view
- Employee management (add/remove)
- Location-based filtering
- Data persistence (SQLite vs Oracle)
- Color coding capabilities
- Modern UI with PyQt6

🔄 **Differences:**
- Uses SQLite instead of Oracle (for local operation)
- Simplified rule system
- Modern Qt-based UI instead of Windows Forms
- Cross-platform compatibility

📋 **Future Enhancements:**
- Advanced rule system (like C# version)
- Import/export functionality
- Multiple view types
- Advanced reporting

   This will:
   - Create a Python virtual environment if needed
   - Install required packages
   - Start the application

2. Alternatively, you can run it manually:
   ```
   python run.py
   ```

## Development

- The application uses PySide6 (Qt for Python) for the GUI
- Database is managed through SQLite
- Configuration is stored in the user's home directory
- Logging is enabled by default in `.taa_app_data/logs/`

## Requirements

- Python 3.8 or newer
- PySide6

## Dependency updates

[Renovate](renovate.json) watches supported dependency manifests once its
[GitHub App](https://github.com/apps/renovate) is installed for this repository.
Routine updates are grouped weekly, with a three-day release-age delay;
vulnerability PRs bypass both restrictions. All updates require manual review and
passing checks; major upgrades first require Dependency Dashboard approval.
