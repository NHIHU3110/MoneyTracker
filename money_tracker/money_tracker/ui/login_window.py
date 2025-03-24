import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QImage, QFont

from money_tracker.utils import load_users
from money_tracker.ui.register_window import RegisterWindow

class LoginWindow(QWidget):
    """Login window for Money Tracker application with custom background"""
    
    def __init__(self):
        super().__init__()
        self.users = load_users()
        self.init_ui()
        
        # Check if we have any users, if not, show a message
        if not self.users:
            QMessageBox.information(self, "Welcome", 
                                  "Welcome to Money Tracker! No accounts exist yet.\n"
                                  "Please click 'Register' to create a new account.")
        
    def init_ui(self):
        self.setWindowTitle("Money Tracker")
        self.setFixedSize(900, 600)
        
        # Set background image using QPalette
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
        bg_path = os.path.join(assets_dir, 'login.png')
        
        # Create background image
        background = QImage(bg_path)
        if not background.isNull():
            palette = QPalette()
            scaled_bg = background.scaled(self.width(), self.height(), 
                                          Qt.AspectRatioMode.IgnoreAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_bg))
            self.setPalette(palette)
        else:
            # Fallback if image can't be loaded
            self.setStyleSheet("""
                QWidget {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                          stop:0 #203b8a, stop:1 #3470c9);
                }
            """)
        
        # Create a white container for login form
        container = QFrame(self)
        container.setGeometry(75, 225, 420, 250)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)
        
        # Username label and field
        username_label = QLabel("Username:", container)
        username_label.setGeometry(0, 50, 110, 30)
        username_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        username_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.username_input = QLineEdit(container)
        self.username_input.setGeometry(150, 50, 170, 30)
        self.username_input.setStyleSheet("""
            background-color: #FFEE99;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Password label and field
        password_label = QLabel("Password:", container)
        password_label.setGeometry(0, 100, 105, 30)
        password_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        password_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.password_input = QLineEdit(container)
        self.password_input.setGeometry(150, 100, 170, 30)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Login button
        self.login_button = QPushButton("Login", container)
        self.login_button.setGeometry(140, 160, 100, 45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d8aee;
            }
        """)
        self.login_button.clicked.connect(self.login)
        
        # Register button
        self.register_button = QPushButton("Register", container)
        self.register_button.setGeometry(270, 160, 100, 45)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d8aee;
            }
        """)
        self.register_button.clicked.connect(self.open_register)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Check if fields are empty
        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both username and password.")
            return
            
        # Reload users in case they were updated
        self.users = load_users()
        
        # Find user
        user = next((u for u in self.users if u.username == username), None)
        
        if user is None:
            # Username doesn't exist
            reply = QMessageBox.question(
                self, "Account Not Found", 
                f"Account with username '{username}' doesn't exist. Would you like to create a new account?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.open_register()
        elif user.password != password:
            # Wrong password
            QMessageBox.warning(self, "Login Failed", "Incorrect password. Please try again.")
        else:
            # Successful login
            try:
                # Defer import to avoid circular import issues
                from money_tracker.ui.main_window import MainWindow
                
                self.main_window = MainWindow(user)
                self.main_window.show()
                self.hide()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while opening the main window: {str(e)}")
                print(f"Error opening main window: {e}")
    
    def open_register(self):
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()