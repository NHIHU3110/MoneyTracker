import sys
import os
from PyQt6.QtWidgets import QApplication

# Ensure the current directory is in the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from money_tracker.ui import LoginWindow

def main():
    """
    Main entry point for the Money Tracker application
    """
    # Create data directory if it doesn't exist
    os.makedirs('money_tracker/data', exist_ok=True)
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the login window
    login_window = LoginWindow()
    login_window.show()
    
    # Enter the application main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()