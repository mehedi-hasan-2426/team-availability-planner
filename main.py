import sys
import os
import traceback

project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.main import main
    
    if __name__ == '__main__':
        main()
        
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure PyQt6 is installed: pip install PyQt6")
    print("Detailed traceback:")
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)
    
except Exception as e:
    print(f"Error: {e}")
    print("Detailed traceback:")
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)