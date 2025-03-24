import uuid
import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QLineEdit, QDateEdit, QRadioButton, QPushButton, QButtonGroup,
    QGridLayout, QWidget, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QDate, QSize , QRect
from PyQt6.QtGui import QPalette, QBrush, QImage, QIcon

from money_tracker.models import Transaction, MTuser_Transaction
from money_tracker.utils.data_handler import save_transactions, save_user_transactions, load_transactions, load_user_transactions

class TransactionDialog(QDialog):
    """Dialog cơ sở cho các giao dịch"""
    def __init__(self, parent, title, category):
        super().__init__(parent)
        self.parent = parent
        self.category = category
        self.setWindowTitle(title)
        self.setFixedSize(400, 350)
        
        # Tạo layout chính
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        
        # Tạo các trường cơ bản
        self.setup_basic_fields()
        
        # Tạo các nút
        self.setup_buttons()
        
        # Thêm form vào layout chính
        self.layout.addLayout(self.form_layout)

    def setup_basic_fields(self):
        # Date field
        self.date_label = QLabel("Date:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            padding: 8px;
            border: 1px solid #2196F3;
            border-radius: 5px;
            background-color: white;
            font-size: 14px;
        """)
        
        # Amount field
        self.amount_label = QLabel("Amount (VND):")
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Enter amount")
        self.amount_edit.setStyleSheet("""
            padding: 8px;
            border: 1px solid #2196F3;
            border-radius: 5px;
            background-color: white;
            font-size: 14px;
        """)
        
        # Add fields to form
        self.form_layout.addRow(self.date_label, self.date_edit)
        self.form_layout.addRow(self.amount_label, self.amount_edit)
    
    def setup_buttons(self):
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        """)
        self.save_button.clicked.connect(self.save_transaction)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        """)
        self.cancel_button.clicked.connect(self.reject)
        
        # Add buttons to layout
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        # Add button layout to main layout
        self.layout.addLayout(button_layout)
    def show_styled_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Show a styled message box with blue background and white text"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        
        # Apply blue background and white text styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1f6aa5;
            }
        """)
        
        return msg_box.exec()

    def validate_input(self):
        """Validate input data"""
        # Check amount
        try:
            amount = float(self.amount_edit.text().replace(',', ''))
            if amount <= 0:
                self.show_styled_message("Error", "Amount must be greater than 0", QMessageBox.Icon.Warning)
                return False
        except ValueError:
            self.show_styled_message("Error", "Invalid amount", QMessageBox.Icon.Warning)
            return False
        
        return True
    
    def save_transaction(self):
        """Save transaction"""
        if not self.validate_input():
            return
        
        # Get data from form
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = float(self.amount_edit.text().replace(',', ''))
        
        # Save transaction
        self.do_save_transaction(date, amount)
        
        # Show success message
        self.show_styled_message("Success", f"Transaction saved successfully")
        
        # Update totals
        if hasattr(self.parent, 'calculate_totals'):
            self.parent.calculate_totals()
        
        # Update UI if needed
        if hasattr(self.parent, 'setup_overview_tab'):
            self.parent.setup_overview_tab()
        
        # Close dialog
        self.accept()


class EarningsDialog(QDialog):
    """Dialog cho thu nhập theo thiết kế mới dựa trên Qt Designer"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Earnings")
        self.setFixedSize(950, 700)  # Kích thước theo mẫu
        
        # # Thiết lập hình nền
        assets_dir = './money_tracker/assets'
        bg_path = os.path.join(assets_dir, 'Earnings.png')
        
        # Đảm bảo có thư mục images trong assets
        self.images_dir = os.path.join(assets_dir, 'images')
        
        # Tạo background
        background = QImage(bg_path)
        if not background.isNull():
            palette = QPalette()
            scaled_bg = background.scaled(self.width(), self.height(), 
                                          Qt.AspectRatioMode.IgnoreAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_bg))
            self.setPalette(palette)
        else:
            # Fallback nếu không tìm thấy hình ảnh
            self.setStyleSheet("""
                QDialog {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                          stop:0 #203b8a, stop:1 #3470c9);
                }
            """)
        
        # Tạo layout chính
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo widget trung tâm 
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tạo các thành phần UI theo file .ui
        self.setup_ui_components(central_layout, assets_dir)
        
        # Thêm central widget vào layout chính
        self.main_layout.addWidget(central_widget)
    
    def setup_ui_components(self, parent_layout, assets_dir):
        """Thiết lập các thành phần UI dựa theo file .ui"""
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                    }
                """)
        form_frame_layout = QVBoxLayout(form_frame)
        form_frame_layout.setContentsMargins(40, 40, 40, 40)
        form_frame_layout.setSpacing(20)

        # Tạo label Amount
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        amount_label.setFixedSize(81, 16)
        amount_label.move(170, 130)
        
        # Tạo text field Amount
        self.line_edit_amount = QLineEdit()
        self.line_edit_amount.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0; /* Nền mặc định */
                border: 2px solid #0066cc; /* Viền */
                border-radius: 10px; /* Bo góc */
                padding: 5px; /* Khoảng cách bên trong */
                color: #333; /* Màu chữ */
                font-size: 16px; /* Kích thước chữ */
            }

            QLineEdit:hover {
                background-color: #ffeb3b; /* Màu vàng nền khi hover */
                border-color: #ffcc00; /* Màu viền khi hover */
            }

            QLineEdit:focus {
                background-color: #ffeb3b; /* Màu vàng nền khi focus */
                border-color: #ffcc00; /* Màu viền khi focus */
            }
        """)
        self.line_edit_amount.setFixedSize(341, 31)
        self.line_edit_amount.move(290, 120)
        
        # Tạo label Date
        date_label = QLabel("Date:")
        date_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        date_label.setFixedSize(81, 16)
        date_label.move(170, 170)

        # tạo date field
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 2px solid #0066cc;
                border-radius: 10px;
                padding: 5px;
                color: #333;
                font-size: 16px;
            }

            QDateEdit:hover {
                border-color: #2196F3;
                background-color: #E3F2FD;
            }

            QDateEdit:focus {
                border-color: #1976D2;
                background-color: #E3F2FD;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #0066cc;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            /* Calendar styling - Blue and White theme */
            QCalendarWidget {
                background-color: #1976D2;  /* Dark blue background */
            }
            
            QCalendarWidget QWidget {
                alternate-background-color: #1976D2;
            }
            
            /* Main view with dates */
            QCalendarWidget QAbstractItemView {
                background-color: #FFFFFF;  /* White background for dates area */
                selection-background-color: #2196F3;  /* Medium blue for selection */
                selection-color: white;
            }
            
            /* Weekday cells */
            QCalendarWidget QAbstractItemView:enabled {
                color: #0D47A1;  /* Dark blue text for regular days */
            }
            
            /* Weekend dates */
            QCalendarWidget QAbstractItemView:!enabled {
                color: #F44336;  /* Red text for weekend days */
            }
            
            /* Hover effect for dates */
            QCalendarWidget QAbstractItemView:hover {
                background-color: #E3F2FD;  /* Light blue background on hover */
                border: 1px solid #2196F3;  /* Medium blue border on hover */
            }
            
            /* Month/year header */
            QCalendarWidget QToolButton {
                color: white;
                background-color: #1976D2;  /* Dark blue for nav bar */
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px;
            }
            
            /* Month/year header hover effect */
            QCalendarWidget QToolButton:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Navigation bar background */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #1976D2;  /* Dark blue for nav bar */
                padding: 4px;
            }
            
            /* Selected date */
            QCalendarWidget QAbstractItemView:item:selected {
                background-color: #2196F3;  /* Medium blue for selection */
                color: white;
            }
            
            /* Calendar arrow buttons */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                color: white;
                background-color: #1976D2;  /* Dark blue for arrows */
                icon-size: 18px;
                padding: 6px;
            }
            
            /* Calendar arrow hover effects */
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Calendar header text (days of week) */
            QCalendarWidget QTableView {
                alternate-background-color: #BBDEFB;  /* Very light blue for alternating items */
            }
            
            /* Today date highlight */
            QCalendarWidget QAbstractItemView:item[today="true"] {
                background-color: #BBDEFB;  /* Very light blue for today */
                font-weight: bold;
                border: 1px solid #1976D2;  /* Dark blue border */
            }
        """)
        
        # Tạo label Category
        category_label = QLabel("Category:")
        category_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        category_label.setFixedSize(131, 31)
        category_label.move(170, 200)
        
        # Tạo layout hình thức grid để đặt các form elements
        form_grid = QGridLayout()
        form_grid.setContentsMargins(0, 0, 0, 0)
        form_grid.setSpacing(10)
        
        form_grid.addWidget(amount_label, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_grid.addWidget(self.line_edit_amount, 0, 1)
        form_grid.addWidget(date_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_grid.addWidget(self.date_edit, 1, 1)
        form_grid.addWidget(category_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        
        form_grid_wrapper = QHBoxLayout()
        form_grid_wrapper.addStretch()
        form_grid_wrapper.addLayout(form_grid)
        form_grid_wrapper.addStretch()

        form_frame_layout.addLayout(form_grid_wrapper)

        
        # Tạo layout cho các category buttons và radio buttons
        category_layout = QGridLayout()
        category_layout.setContentsMargins(50, 10, 50, 10)
        category_layout.setHorizontalSpacing(80)
        category_layout.setVerticalSpacing(5)
        
        # Button style
        button_style = """
            QPushButton {
                background-color: #0066cc; 
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffcc00;
            }
            QPushButton:pressed {
                background-color: #ff9900;
            }
        """
        
        # Radio button style
        radio_style = """
            QRadioButton {
                font-size: 16px;
                font-weight: bold;
                color: rgb(11, 37, 114);
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
        """
        
        # Button group cho radio buttons
        self.category_group = QButtonGroup()
        
        # Tạo các buttons và radio buttons
        # 1. Salary
        self.push_button1 = QPushButton()
        self.push_button1.setFixedSize(91, 81)
        self.push_button1.setStyleSheet(button_style)
        salary_icon_path = os.path.join(assets_dir, "salary_icon.png")
        if os.path.exists(salary_icon_path):
            self.push_button1.setIcon(QIcon(salary_icon_path))
            self.push_button1.setIconSize(QSize(70, 70))
        
        self.radio_salary = QRadioButton("Salary")
        self.radio_salary.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_salary, 1)
        
        # 2. Allowance
        self.push_button2 = QPushButton()
        self.push_button2.setFixedSize(91, 81)
        self.push_button2.setStyleSheet(button_style)
        allowance_icon_path = os.path.join(assets_dir, "allowance_icon.png")
        if os.path.exists(allowance_icon_path):
            self.push_button2.setIcon(QIcon(allowance_icon_path))
            self.push_button2.setIconSize(QSize(70, 70))
        
        self.radio_allowance = QRadioButton("Allowance")
        self.radio_allowance.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_allowance, 2)
        
        # 3. Others
        self.push_button3 = QPushButton()
        self.push_button3.setFixedSize(91, 81)
        self.push_button3.setStyleSheet(button_style)
        others_icon_path = os.path.join(assets_dir, "others_income_icon.png")
        if os.path.exists(others_icon_path):
            self.push_button3.setIcon(QIcon(others_icon_path))
            self.push_button3.setIconSize(QSize(70, 70))
        
        self.radio_others = QRadioButton("Others")
        self.radio_others.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_others, 3)
        
        # Kết nối buttons với radio buttons
        self.push_button1.clicked.connect(lambda: self.radio_salary.setChecked(True))
        self.push_button2.clicked.connect(lambda: self.radio_allowance.setChecked(True))
        self.push_button3.clicked.connect(lambda: self.radio_others.setChecked(True))
        
        # Thêm vào layout
        category_layout.addWidget(self.push_button1, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button2, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button3, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_salary, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_allowance, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_others, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_frame_layout.addLayout(category_layout)

        
        # Tạo layout cho các nút hành động
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(50, 20, 50, 20)
        action_layout.setSpacing(50)
        
        # Action button style
        action_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 2px solid #2980b9;
                border-radius: 15px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085);
                color: white;
                border-color: #16a085;
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c);
                border-color: #1abc9c;
                color: white;
            }
        """
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(113, 51)
        self.clear_button.setStyleSheet(action_button_style)
        self.clear_button.clicked.connect(self.clear_form)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(113, 51)
        self.save_button.setStyleSheet(action_button_style)
        self.save_button.clicked.connect(self.save_transaction)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(113, 51)
        self.close_button.setStyleSheet(action_button_style)
        self.close_button.clicked.connect(self.reject)
        
        # Thêm các buttons vào layout
        action_layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_frame_layout.addLayout(action_layout)

        parent_layout.addWidget(form_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        # Đặt radio mặc định
        self.radio_salary.setChecked(False)
    
    def show_styled_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Show a styled message box with blue background and white text"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        
        # Apply blue background and white text styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1f6aa5;
            }
        """)
        
        return msg_box.exec()
    def clear_form(self):
        """Xóa dữ liệu form"""
        self.line_edit_amount.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.radio_salary.setChecked(True)
    
    def validate_input(self):
        """Validate input data"""
        # Check amount
        try:
            amount = float(self.line_edit_amount.text().replace(',', ''))
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount"
        
        return True, ""
    
    def save_transaction(self):
        """Save transaction"""
        # Validate data
        valid, message = self.validate_input()
        if not valid:
            self.show_styled_message("Error", message, QMessageBox.Icon.Warning)
            return
        
        # Get data from form
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = float(self.line_edit_amount.text().replace(',', ''))
        
        # Get income type
        category_detail = "Salary"  # Default
        if self.radio_allowance.isChecked():
            category_detail = "Allowance"
        elif self.radio_others.isChecked():
            category_detail = "Others"
        
        # Create new transaction
        transaction = Transaction(
            transaction_number=str(uuid.uuid4()),
            transaction_date=date,
            amount=amount,
            category="Money In",
            category_detail=category_detail
        )
        
        # Load existing data
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        # Add to transaction list
        transactions.append(transaction)
        
        # Save to user transaction list
        user_transaction = MTuser_Transaction(
            transaction_number=transaction.transaction_number,
            name=self.parent.user.name
        )
        user_transactions.append(user_transaction)
        
        # Save to file
        save_transactions(transactions)
        save_user_transactions(user_transactions)
        
        # Show success message
        self.show_styled_message("Success", "Income transaction saved successfully")
        
        # Update UI if needed
        if hasattr(self.parent, 'setup_overview_tab'):
            self.parent.setup_overview_tab()
        
        # Clear form
        self.clear_form()

class SpendingDialog(QDialog):
    """Dialog cho chi tiêu theo thiết kế mới dựa trên Qt Designer"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Spending")
        self.setFixedSize(950, 700)  # Kích thước theo mẫu
        
        # Thiết lập hình nền
        assets_dir = './money_tracker/assets'
        bg_path = os.path.join(assets_dir, 'Spending.png')
        
        # Đảm bảo có thư mục images trong assets
        self.images_dir = os.path.join(assets_dir, 'images')
        
        # Tạo background
        background = QImage(bg_path)
        if not background.isNull():
            palette = QPalette()
            scaled_bg = background.scaled(self.width(), self.height(), 
                                          Qt.AspectRatioMode.IgnoreAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_bg))
            self.setPalette(palette)
        else:
            # Fallback nếu không tìm thấy hình ảnh
            self.setStyleSheet("""
                QDialog {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                          stop:0 #1565c0, stop:1 #64b5f6);

                }
            """)
        
        # Tạo layout chính
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo widget trung tâm 
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tạo các thành phần UI theo file .ui
        self.setup_ui_components(central_layout, assets_dir)
        
        # Thêm central widget vào layout chính
        self.main_layout.addWidget(central_widget)
    
    def setup_ui_components(self, parent_layout, assets_dir):
        form_frame = QFrame()
        form_frame.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 25px;
            }
        """)
        form_frame_layout = QVBoxLayout(form_frame)
        form_frame_layout.setContentsMargins(40, 40, 40, 40)
        form_frame_layout.setSpacing(20)
        """Thiết lập các thành phần UI dựa theo file .ui"""
        # Tạo label Amount
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        amount_label.setFixedSize(81, 16)
        amount_label.move(170, 130)
        
        # Tạo text field Amount
        self.line_edit_amount = QLineEdit()
        self.line_edit_amount.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0; /* Nền mặc định */
                border: 2px solid #0066cc; /* Viền */
                border-radius: 10px; /* Bo góc */
                padding: 5px; /* Khoảng cách bên trong */
                color: #333; /* Màu chữ */
                font-size: 16px; /* Kích thước chữ */
            }

            QLineEdit:hover {
                background-color: #ffeb3b; /* Màu vàng nền khi hover */
                border-color: #ffcc00; /* Màu viền khi hover */
            }

            QLineEdit:focus {
                background-color: #ffeb3b; /* Màu vàng nền khi focus */
                border-color: #ffcc00; /* Màu viền khi focus */
            }
        """)
        self.line_edit_amount.setFixedSize(341, 31)
        self.line_edit_amount.move(290, 120)
        
        # Tạo label Date
        date_label = QLabel("Date:")
        date_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        date_label.setFixedSize(81, 16)
        date_label.move(170, 170)
        
        # Tạo date field
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 2px solid #0066cc;
                border-radius: 10px;
                padding: 5px;
                color: #333;
                font-size: 16px;
            }

            QDateEdit:hover {
                border-color: #2196F3;
                background-color: #E3F2FD;
            }

            QDateEdit:focus {
                border-color: #1976D2;
                background-color: #E3F2FD;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #0066cc;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            /* Calendar styling - Blue and White theme */
            QCalendarWidget {
                background-color: #1976D2;  /* Dark blue background */
            }
            
            QCalendarWidget QWidget {
                alternate-background-color: #1976D2;
            }
            
            /* Main view with dates */
            QCalendarWidget QAbstractItemView {
                background-color: #FFFFFF;  /* White background for dates area */
                selection-background-color: #2196F3;  /* Medium blue for selection */
                selection-color: white;
            }
            
            /* Weekday cells */
            QCalendarWidget QAbstractItemView:enabled {
                color: #0D47A1;  /* Dark blue text for regular days */
            }
            
            /* Weekend dates */
            QCalendarWidget QAbstractItemView:!enabled {
                color: #F44336;  /* Red text for weekend days */
            }
            
            /* Hover effect for dates */
            QCalendarWidget QAbstractItemView:hover {
                background-color: #E3F2FD;  /* Light blue background on hover */
                border: 1px solid #2196F3;  /* Medium blue border on hover */
            }
            
            /* Month/year header */
            QCalendarWidget QToolButton {
                color: white;
                background-color: #1976D2;  /* Dark blue for nav bar */
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px;
            }
            
            /* Month/year header hover effect */
            QCalendarWidget QToolButton:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Navigation bar background */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #1976D2;  /* Dark blue for nav bar */
                padding: 4px;
            }
            
            /* Selected date */
            QCalendarWidget QAbstractItemView:item:selected {
                background-color: #2196F3;  /* Medium blue for selection */
                color: white;
            }
            
            /* Calendar arrow buttons */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                color: white;
                background-color: #1976D2;  /* Dark blue for arrows */
                icon-size: 18px;
                padding: 6px;
            }
            
            /* Calendar arrow hover effects */
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Calendar header text (days of week) */
            QCalendarWidget QTableView {
                alternate-background-color: #BBDEFB;  /* Very light blue for alternating items */
            }
            
            /* Today date highlight */
            QCalendarWidget QAbstractItemView:item[today="true"] {
                background-color: #BBDEFB;  /* Very light blue for today */
                font-weight: bold;
                border: 1px solid #1976D2;  /* Dark blue border */
            }
        """)
        
        # Tạo label Category
        category_label = QLabel("Category:")
        category_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
        """)
        category_label.setFixedSize(131, 31)
        category_label.move(170, 200)
        
        # Tạo layout hình thức grid để đặt các form elements
        form_grid = QGridLayout()
        form_grid.setContentsMargins(0, 0, 0, 0)
        form_grid.setSpacing(10)
        
        form_grid.addWidget(amount_label, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_grid.addWidget(self.line_edit_amount, 0, 1)
        form_grid.addWidget(date_label, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_grid.addWidget(self.date_edit, 1, 1)
        form_grid.addWidget(category_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        
        form_grid_wrapper = QHBoxLayout()
        form_grid_wrapper.addStretch()
        form_grid_wrapper.addLayout(form_grid)
        form_grid_wrapper.addStretch()

        form_frame_layout.addLayout(form_grid_wrapper)

        
        # Tạo layout cho các category buttons và radio buttons
        category_layout = QGridLayout()
        category_layout.setContentsMargins(20, 10, 20, 10)
        category_layout.setHorizontalSpacing(30)
        category_layout.setVerticalSpacing(5)
        
        # Button style
        button_style = """
            QPushButton {
                background-color: #0066cc; 
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffcc00;
            }
            QPushButton:pressed {
                background-color: #ff9900;
            }
        """
        
        # Radio button style
        radio_style = """
            QRadioButton {
                font-size: 16px;
                font-weight: bold;
                color: rgb(11, 37, 114);
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
        """
        
        # Button group cho radio buttons
        self.category_group = QButtonGroup()
        
        # Tạo các buttons và radio buttons
        # 1. Food and Drink
        self.push_button_food = QPushButton()
        self.push_button_food.setFixedSize(81, 81)
        self.push_button_food.setStyleSheet(button_style)
        food_icon_path = os.path.join(assets_dir, "food_and_drink.png")
        if os.path.exists(food_icon_path):
            self.push_button_food.setIcon(QIcon(food_icon_path))
            self.push_button_food.setIconSize(QSize(80, 80))
        
        self.radio_food = QRadioButton("Food and drink")
        self.radio_food.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_food, 1)
        
        # 2. Moving
        self.push_button_moving = QPushButton()
        self.push_button_moving.setFixedSize(81, 81)
        self.push_button_moving.setStyleSheet(button_style)
        moving_icon_path = os.path.join(assets_dir, "moving.png")
        if os.path.exists(moving_icon_path):
            self.push_button_moving.setIcon(QIcon(moving_icon_path))
            self.push_button_moving.setIconSize(QSize(80, 80))
        
        self.radio_moving = QRadioButton("Moving")
        self.radio_moving.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_moving, 2)
        
        # 3. Shopping
        self.push_button_shopping = QPushButton()
        self.push_button_shopping.setFixedSize(81, 81)
        self.push_button_shopping.setStyleSheet(button_style)
        shopping_icon_path = os.path.join(assets_dir, "shopping.png")
        if os.path.exists(shopping_icon_path):
            self.push_button_shopping.setIcon(QIcon(shopping_icon_path))
            self.push_button_shopping.setIconSize(QSize(80, 80))
        
        self.radio_shopping = QRadioButton("Shopping")
        self.radio_shopping.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_shopping, 3)
        
        # 4. Invoice
        self.push_button_invoice = QPushButton()
        self.push_button_invoice.setFixedSize(81, 81)
        self.push_button_invoice.setStyleSheet(button_style)
        invoice_icon_path = os.path.join(assets_dir, "invoice.png")
        if os.path.exists(invoice_icon_path):
            self.push_button_invoice.setIcon(QIcon(invoice_icon_path))
            self.push_button_invoice.setIconSize(QSize(80, 80))
        
        self.radio_invoice = QRadioButton("Invoice")
        self.radio_invoice.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_invoice, 4)
        
        # 5. Others
        self.push_button_others = QPushButton()
        self.push_button_others.setFixedSize(81, 81)
        self.push_button_others.setStyleSheet(button_style)
        others_icon_path = os.path.join(assets_dir, "chi.png")
        if os.path.exists(others_icon_path):
            self.push_button_others.setIcon(QIcon(others_icon_path))
            self.push_button_others.setIconSize(QSize(80, 80))
        
        self.radio_others = QRadioButton("Others")
        self.radio_others.setStyleSheet(radio_style)
        self.category_group.addButton(self.radio_others, 5)
        
        # Kết nối buttons với radio buttons
        self.push_button_food.clicked.connect(lambda: self.radio_food.setChecked(True))
        self.push_button_moving.clicked.connect(lambda: self.radio_moving.setChecked(True))
        self.push_button_shopping.clicked.connect(lambda: self.radio_shopping.setChecked(True))
        self.push_button_invoice.clicked.connect(lambda: self.radio_invoice.setChecked(True))
        self.push_button_others.clicked.connect(lambda: self.radio_others.setChecked(True))
        
        # Thêm vào layout
        category_layout.addWidget(self.push_button_food, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button_moving, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button_shopping, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button_invoice, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.push_button_others, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        
        category_layout.addWidget(self.radio_food, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_moving, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_shopping, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_invoice, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        category_layout.addWidget(self.radio_others, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_frame_layout.addLayout(category_layout)
        
        # Tạo layout cho các nút hành động
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(50, 20, 50, 20)
        action_layout.setSpacing(50)
        
        # Action button style
        action_button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 2px solid #2980b9;
                border-radius: 15px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #16a085);
                color: white;
                border-color: #16a085;
            }

            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #16a085, stop:1 #1abc9c);
                border-color: #1abc9c;
                color: white;
            }
        """
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(113, 51)
        self.clear_button.setStyleSheet(action_button_style)
        self.clear_button.clicked.connect(self.clear_form)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(113, 51)
        self.save_button.setStyleSheet(action_button_style)
        self.save_button.clicked.connect(self.save_transaction)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(113, 51)
        self.close_button.setStyleSheet(action_button_style)
        self.close_button.clicked.connect(self.reject)
        
        # Thêm các buttons vào layout
        action_layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_frame_layout.addLayout(action_layout)
        parent_layout.addWidget(form_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        # Đặt radio mặc định
        self.radio_food.setChecked(False)
    
    def clear_form(self):
        """Xóa dữ liệu form"""
        self.line_edit_amount.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.radio_food.setChecked(True)
    
    def validate_input(self):
        """Validate input data"""
        # Check amount
        try:
            amount = float(self.line_edit_amount.text().replace(',', ''))
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount"
        
        return True, ""
    
    def save_transaction(self):
        """Save transaction"""
        # Validate data
        valid, message = self.validate_input()
        if not valid:
            self.show_styled_message("Error", message, QMessageBox.Icon.Warning)
            return
        
        # Get data from form
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = float(self.line_edit_amount.text().replace(',', ''))
        
        # Get expense type
        category_detail = "Food and drink"  # Default
        if self.radio_moving.isChecked():
            category_detail = "Moving"
        elif self.radio_shopping.isChecked():
            category_detail = "Shopping"
        elif self.radio_invoice.isChecked():
            category_detail = "Invoice"
        elif self.radio_others.isChecked():
            category_detail = "Others"
        
        # Create new transaction
        transaction = Transaction(
            transaction_number=str(uuid.uuid4()),
            transaction_date=date,
            amount=amount,
            category="Money Out",
            category_detail=category_detail
        )
        
        # Load existing data
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        # Add to transaction list
        transactions.append(transaction)
        
        # Save to user transaction list
        user_transaction = MTuser_Transaction(
            transaction_number=transaction.transaction_number,
            name=self.parent.user.name
        )
        user_transactions.append(user_transaction)
        
        # Save to file
        save_transactions(transactions)
        save_user_transactions(user_transactions)
        
        # Show success message
        self.show_styled_message("Success", "Expense transaction saved successfully")
        
        # Update UI if needed
        if hasattr(self.parent, 'setup_overview_tab'):
            self.parent.setup_overview_tab()
        
        # Clear form
        self.clear_form()
       
    def show_styled_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Show a styled message box with blue background and white text"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        
        # Apply blue background and white text styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1f6aa5;
            }
        """)
        
        return msg_box.exec()


class SavingsDialog(QDialog):
    """Dialog cho tiết kiệm theo thiết kế mới dựa trên Qt Designer"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Savings")
        self.setFixedSize(837, 485)  # Kích thước theo mẫu .ui
        
        # Thiết lập hình nền
        assets_dir = './money_tracker/assets'
        bg_path = os.path.join(assets_dir, 'Saving.png')
        
        # Đảm bảo có thư mục images trong assets
        self.images_dir = os.path.join(assets_dir, 'images')
        
        # Tạo background
        background = QImage(bg_path)
        if not background.isNull():
            palette = QPalette()
            scaled_bg = background.scaled(self.width(), self.height(), 
                                          Qt.AspectRatioMode.IgnoreAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_bg))
            self.setPalette(palette)
        else:
            # Fallback nếu không tìm thấy hình ảnh
            self.setStyleSheet("""
                QDialog {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                          stop:0 #00695c, stop:1 #4db6ac);
                }
            """)
        
        # Tạo layout chính
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tạo widget trung tâm 
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tạo các thành phần UI theo file .ui
        self.setup_ui_components(central_layout)
        
        # Thêm central widget vào layout chính
        self.main_layout.addWidget(central_widget)
    
    def setup_ui_components(self, parent_layout):
        """Thiết lập các thành phần UI dựa theo file .ui"""
        # Tạo layout form
        form_layout = QGridLayout()
        form_layout.setContentsMargins(80, 150, 80, 20)  # Tăng top margin lên 150px
        form_layout.setSpacing(20)
        
        # Tạo label Amount
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
        """)
        
        # Tạo text field Amount
        self.line_edit_amount = QLineEdit()
        self.line_edit_amount.setStyleSheet("""
            QLineEdit {
                background-color: #FFEB3B; /* Nền màu vàng như trong hình */
                border: 2px solid #0066cc; /* Viền */
                border-radius: 10px; /* Bo góc */
                padding: 5px; /* Khoảng cách bên trong */
                color: #333; /* Màu chữ */
                font-size: 16px; /* Kích thước chữ */
                transition: background 0.3s ease; /* Thêm hiệu ứng chuyển màu nền */
            }

            QLineEdit:hover {
                background-color: #FFF59D; /* Màu vàng nhạt hơn khi hover */
                border-color: #ffcc00; /* Màu viền khi hover */
            }

            QLineEdit:focus {
                background-color: #FFEB3B; /* Màu vàng khi focus */
                border-color: #ffcc00; /* Màu viền khi focus */
            }
        """)
        
        # Tạo label Date
        date_label = QLabel("Date:")
        date_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #333;
        """)
        
        # Tạo date field
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 2px solid #0066cc;
                border-radius: 10px;
                padding: 5px;
                color: #333;
                font-size: 16px;
            }

            QDateEdit:hover {
                border-color: #2196F3;
                background-color: #E3F2FD;
            }

            QDateEdit:focus {
                border-color: #1976D2;
                background-color: #E3F2FD;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #0066cc;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            
            /* Calendar styling - Blue and White theme */
            QCalendarWidget {
                background-color: #1976D2;  /* Dark blue background */
            }
            
            QCalendarWidget QWidget {
                alternate-background-color: #1976D2;
            }
            
            /* Main view with dates */
            QCalendarWidget QAbstractItemView {
                background-color: #FFFFFF;  /* White background for dates area */
                selection-background-color: #2196F3;  /* Medium blue for selection */
                selection-color: white;
            }
            
            /* Weekday cells */
            QCalendarWidget QAbstractItemView:enabled {
                color: #0D47A1;  /* Dark blue text for regular days */
            }
            
            /* Weekend dates */
            QCalendarWidget QAbstractItemView:!enabled {
                color: #F44336;  /* Red text for weekend days */
            }
            
            /* Hover effect for dates */
            QCalendarWidget QAbstractItemView:hover {
                background-color: #E3F2FD;  /* Light blue background on hover */
                border: 1px solid #2196F3;  /* Medium blue border on hover */
            }
            
            /* Month/year header */
            QCalendarWidget QToolButton {
                color: white;
                background-color: #1976D2;  /* Dark blue for nav bar */
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
                padding: 6px;
            }
            
            /* Month/year header hover effect */
            QCalendarWidget QToolButton:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Navigation bar background */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #1976D2;  /* Dark blue for nav bar */
                padding: 4px;
            }
            
            /* Selected date */
            QCalendarWidget QAbstractItemView:item:selected {
                background-color: #2196F3;  /* Medium blue for selection */
                color: white;
            }
            
            /* Calendar arrow buttons */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                color: white;
                background-color: #1976D2;  /* Dark blue for arrows */
                icon-size: 18px;
                padding: 6px;
            }
            
            /* Calendar arrow hover effects */
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #2196F3;  /* Medium blue on hover */
            }
            
            /* Calendar header text (days of week) */
            QCalendarWidget QTableView {
                alternate-background-color: #BBDEFB;  /* Very light blue for alternating items */
            }
            
            /* Today date highlight */
            QCalendarWidget QAbstractItemView:item[today="true"] {
                background-color: #BBDEFB;  /* Very light blue for today */
                font-weight: bold;
                border: 1px solid #1976D2;  /* Dark blue border */
            }
        """)
        
        # Thêm vào layout với khoảng cách
        form_layout.addWidget(amount_label, 0, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.line_edit_amount, 0, 1)
        # Thêm khoảng cách giữa Amount và Date
        form_layout.setRowMinimumHeight(1, 25)
        form_layout.addWidget(date_label, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(self.date_edit, 2, 1)
        
        parent_layout.addLayout(form_layout)
        
        # Tạo layout cho các nút hành động
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(50, 20, 50, 20) 
        action_layout.setSpacing(80)
        
        # Button style cho các nút action - cập nhật màu theo hình
        button_style = """
            /* Tùy chỉnh cho các nút */
            QPushButton {
                background: #3498db; /* Màu xanh như trong hình */
                color: white; /* Màu chữ */
                border: none; /* Không viền */
                border-radius: 20px; /* Bo tròn góc của nút */
                padding: 15px 30px; /* Khoảng cách giữa văn bản và viền */
                font-size: 16px; /* Kích thước font chữ */
                font-weight: bold; /* Làm cho chữ đậm */
                transition: background-color 0.3s; /* Hiệu ứng chuyển màu */
            }

            QPushButton:hover {
                background: #2980b9; /* Màu xanh đậm hơn khi hover */
                color: white; /* Màu chữ khi hover */
            }

            QPushButton:pressed {
                background: #1f6aa5; /* Màu xanh đậm hơn nữa khi nhấn */
                color: white; /* Màu chữ khi nhấn */
            }
        """
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(113, 51)
        self.clear_button.setStyleSheet(button_style)
        self.clear_button.clicked.connect(self.clear_form)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(113, 51)
        self.save_button.setStyleSheet(button_style)
        self.save_button.clicked.connect(self.save_transaction)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setFixedSize(113, 51)
        self.close_button.setStyleSheet(button_style)
        self.close_button.clicked.connect(self.reject)
        
        # Thêm các buttons vào layout
        action_layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        action_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        parent_layout.addLayout(action_layout)
        


    def clear_form(self):
        """Xóa dữ liệu form"""
        self.line_edit_amount.clear()
        self.date_edit.setDate(QDate.currentDate())
    
    def validate_input(self):
        """Validate input data"""
        # Check amount
        try:
            amount = float(self.line_edit_amount.text().replace(',', ''))
            if amount <= 0:
                return False, "Amount must be greater than 0"
        except ValueError:
            return False, "Invalid amount"
        
        return True, ""
    
    def save_transaction(self):
        """Save transaction"""
        # Validate data
        valid, message = self.validate_input()
        if not valid:
            self.show_styled_message("Error", message, QMessageBox.Icon.Warning)
            return
        
        # Get data from form
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = float(self.line_edit_amount.text().replace(',', ''))
        
        # Create new transaction
        transaction = Transaction(
            transaction_number=str(uuid.uuid4()),
            transaction_date=date,
            amount=amount,
            category="Savings",
            category_detail="General Savings"  # Default only one savings type
        )
        
        # Load existing data
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        # Add to transaction list
        transactions.append(transaction)
        
        # Save to user transaction list
        user_transaction = MTuser_Transaction(
            transaction_number=transaction.transaction_number,
            name=self.parent.user.name
        )
        user_transactions.append(user_transaction)
        
        # Save to file
        save_transactions(transactions)
        save_user_transactions(user_transactions)
        
        # Show success message
        self.show_styled_message("Success", "Savings transaction saved successfully")
        
        # Update UI if needed
        if hasattr(self.parent, 'setup_overview_tab'):
            self.parent.setup_overview_tab()
        
        # Clear form
        self.clear_form()
    
    def show_styled_message(self, title, message, icon_type=QMessageBox.Icon.Information):
        """Show a styled message box with blue background and white text"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        
        # Apply blue background and white text styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3498db;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1f6aa5;
            }
        """)
        
        return msg_box.exec()


# Các phương thức để hiển thị các dialog trong MainWindow
def show_earnings_form(self):
    """Hiển thị form thu nhập"""
    dialog = EarningsDialog(self)
    dialog.exec()

def show_spending_form(self):
    """Hiển thị form chi tiêu"""
    dialog = SpendingDialog(self)
    dialog.exec()
    
def show_savings_form(self):
    """Hiển thị form tiết kiệm"""
    dialog = SavingsDialog(self)
    dialog.exec()