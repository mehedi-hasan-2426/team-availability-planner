import os
import sys

project_dir = os.path.dirname(os.path.abspath(__file__))

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

try:
    from src.main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    input("Press Enter to exit...")
    sys.exit(1)
    
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
    sys.exit(1)
