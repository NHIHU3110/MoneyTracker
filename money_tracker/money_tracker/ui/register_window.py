import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QImage, QFont

from money_tracker.utils import load_users, save_users
from money_tracker.models import MTuser

class RegisterWindow(QWidget):
    """
    Registration window for Money Tracker application
    """
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.users = load_users()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Money Tracker - Register")
        self.setFixedSize(900, 600)
        
        # Set background image using QPalette
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
        bg_path = os.path.join(assets_dir, 'register.png')  # Using the same background as login
        
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
        
        # # Create a container with "REGISTER" title at top
        # title_label = QLabel("REGISTER", self)
        # title_label.setGeometry(0, 80, 900, 100)
        # title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # title_label.setStyleSheet("""
        #     font-size: 72px;
        #     font-weight: bold;
        #     color: white;
        #     text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        # """)
        
        # Create a white container for register form - sized to match the image exactly
        container = QFrame(self)
        container.setGeometry(205, 165, 470, 370)  # Made slightly taller to accommodate buttons
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)
        
        # Name label and field - positioned exactly as in the image
        name_label = QLabel("Name:", container)
        name_label.setGeometry(30, 30, 100, 25)
        name_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        
        self.name_input = QLineEdit(container)
        self.name_input.setGeometry(30, 60, 390, 35)
        self.name_input.setStyleSheet("""
            background-color: #FFEE99;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Username label and field
        username_label = QLabel("Username:", container)
        username_label.setGeometry(30, 100, 100, 25)
        username_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        
        self.username_input = QLineEdit(container)
        self.username_input.setGeometry(30, 130, 390, 35)
        self.username_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Password label and field
        password_label = QLabel("Password:", container)
        password_label.setGeometry(30, 170, 100, 25)
        password_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        
        self.password_input = QLineEdit(container)
        self.password_input.setGeometry(30, 200, 390, 35)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Re-enter Password label and field
        repass_label = QLabel("Re-enter password:", container)
        repass_label.setGeometry(30, 240, 150, 25)
        repass_label.setStyleSheet("""
            font-size: 16px;
            font-weight: normal;
            color: black;
        """)
        
        self.repass_input = QLineEdit(container)
        self.repass_input.setGeometry(30, 270, 390, 35)
        self.repass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.repass_input.setStyleSheet("""
            background-color: white;
            border: 1px solid #2196F3;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        
        # Button style - consistent for both buttons
        button_style = """
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
        """
        
        # Position buttons centered at bottom with spacing - similar to the image
        self.back_button = QPushButton("Back", container)
        self.back_button.setGeometry(100, 320, 120, 40)
        self.back_button.setStyleSheet(button_style)
        self.back_button.clicked.connect(self.go_back)
        
        self.enter_button = QPushButton("Enter", container)
        self.enter_button.setGeometry(240, 320, 120, 40)
        self.enter_button.setStyleSheet(button_style)
        self.enter_button.clicked.connect(self.register)
        
    def go_back(self):
        self.login_window.show()
        self.hide()
        
    def register(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        repassword = self.repass_input.text()
        
        # Validate inputs
        if not name or not username or not password or not repassword:
            QMessageBox.warning(self, "Registration Error", "Please fill in all fields.")
            return
            
        # Check if username exists
        if any(u.username == username for u in self.users):
            QMessageBox.warning(self, "Registration Error", f"Username '{username}' already exists.")
            return
            
        # Check if passwords match
        if password != repassword:
            QMessageBox.warning(self, "Registration Error", "Passwords do not match.")
            return
            
        # Create new user
        new_user = MTuser(name, username, password)
        self.users.append(new_user)
        save_users(self.users)
        
        QMessageBox.information(self, "Registration Successful", 
                               f"Account for {name} created successfully. You can now log in.")
        
        self.login_window.users = self.users  # Update users in login window
        self.go_back()