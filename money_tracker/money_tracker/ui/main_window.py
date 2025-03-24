import os

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QMessageBox, QTabWidget, QFrame, QLineEdit,
    QStackedWidget, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QImage, QPixmap
from money_tracker.ui.dialogs.Dialogs import (
    EarningsDialog, SpendingDialog, SavingsDialog
)
from money_tracker.utils import (
    load_transactions, save_transactions,
    load_user_transactions, save_user_transactions
)
from money_tracker.ui.management_tab import ManagementTab

class MainWindow(QMainWindow):
    """
    Main window for Money Tracker application
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        
        self.transactions = load_transactions()
        self.user_transactions = load_user_transactions()

        #self.setup_management_tab()
        # Initialize UI
        self.init_ui()
                
    def init_ui(self):
        self.setWindowTitle("Money Tracker")
        self.setMinimumSize(900, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Set background image using QPalette
        assets_dir = './money_tracker/assets'
        bg_path = os.path.join(assets_dir, 'MainWindow.png')  # Reusing login background
        
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
            
        # Create main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.addSpacing(0)
        # Create tab bar - match exactly the style in the screenshot
        self.tab_widget = QTabWidget()
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tab_widget.setMinimumHeight(50)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: transparent;
            }
            QTabBar::tab {
                background: #1a3c6d;
                color: white;
                border: 2px solid #1a3c6d;
                border-radius: 0px;
                padding: 10px 20px;
                margin-right: 0px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: white;
                border-color: #4a90e2;
            }
            QTabBar::tab:hover {
                background-color: #76d7c4;
                border-color: #76d7c4;
            }
        """)
        
        # Create tab pages
        overview_tab = QWidget()
        new_transaction_tab = QWidget()
        management_tab = QWidget()
        history_tab = QWidget()
        setting_tab = QWidget()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(overview_tab, "Overview")
        self.tab_widget.addTab(new_transaction_tab, "New Transaction")
        self.tab_widget.addTab(management_tab, "Management")
        self.tab_widget.addTab(history_tab, "History")
        self.tab_widget.addTab(setting_tab, "Setting")
        
        # Connect tab changed signal
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # Add tab widget to main layout
        tab_wrapper = QHBoxLayout()
        tab_wrapper.addStretch()
        tab_wrapper.addWidget(self.tab_widget)
        tab_wrapper.addStretch()
        main_layout.addLayout(tab_wrapper)

        
        # Create white content container
        self.content_container = QWidget()
        self.content_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
  # Set fixed height
        self.content_container.setStyleSheet("""
            background-color: white;
            border-top-left-radius: 0px;
            border-top-right-radius: 0px;
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            margin: 0px 20px 20px 20px;
        """)
        
        # Create stacked widget to hold different tab contents
        self.stacked_widget = QStackedWidget(self.content_container)
        
        # Create content widgets for each tab
        self.overview_content = QWidget()
        self.new_transaction_content = QWidget()
        self.management_content = QWidget()
        self.history_content = QWidget()
        self.setting_content = QWidget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.overview_content)
        self.stacked_widget.addWidget(self.new_transaction_content)
        self.stacked_widget.addWidget(self.management_content)
        self.stacked_widget.addWidget(self.history_content)
        self.stacked_widget.addWidget(self.setting_content)
        
        # Set layout for content container
        content_layout = QVBoxLayout(self.content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stacked_widget)
        
        # Setup tab contents
        self.setup_overview_tab()
        self.setup_new_transaction_tab()
        self.setup_history_tab()  
        self.setup_management_tab()
        self.setup_setting_tab()  

        
        # Add content container to main layout
        main_layout.addWidget(self.content_container)
        
        # Set central widget
        self.setCentralWidget(central_widget)
        
    def tab_changed(self, index):
        """Handle tab changes"""
        self.stacked_widget.setCurrentIndex(index)
        
        if index == 0:  # Overview tab
            self.setup_overview_tab()
        elif index == 2 and hasattr(self, 'management_tab'):  # Management tab
            self.management_tab.refresh_charts()
        elif index == 3 and hasattr(self, 'history_tab_widget'):  # History tab
            self.force_refresh_history_tab()
    
    def setup_new_transaction_tab(self):
        """Setup the New Transaction tab content với ba danh mục chính"""
        layout = QVBoxLayout(self.new_transaction_content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tạo khung nền trắng
        bg_frame = QFrame()
        bg_frame.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
        """)
        
        # Layout cho khung nền
        bg_layout = QVBoxLayout(bg_frame)
        bg_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tạo layout ngang cho ba danh mục
        categories_layout = QHBoxLayout()
        categories_layout.setSpacing(20)
        
        earnings_widget = self.create_category_button("Earnings", "earnings_icon.png")
        
        spending_widget = self.create_category_button("Spending", "spending_icon.png")
        
        savings_widget = self.create_category_button("Savings", "savings_icon.png")
        
        # Thêm widget vào layout
        categories_layout.addWidget(earnings_widget)
        categories_layout.addWidget(spending_widget)
        categories_layout.addWidget(savings_widget)
        
        # Thêm layout vào khung nền
        bg_layout.addLayout(categories_layout)
        
        # Thêm khung nền vào layout chính
        layout.addWidget(bg_frame)

    def create_category_button(self, label_text, icon_path):
        """Tạo nút danh mục với icon và nhãn"""
        # Tạo widget
        widget = QWidget()
        widget.setCursor(Qt.CursorShape.PointingHandCursor)  # Đổi con trỏ thành bàn tay khi di chuột qua
        
        # Tạo layout
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tải icon
        assets_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets'))
        icon_full_path = os.path.join(assets_dir, icon_path)
        
        # Tạo nhãn icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_full_path).scaled(
            150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tạo nhãn văn bản
        text_label = QLabel(label_text)
        text_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: #3498db;
            padding: 10px 20px;
            border-radius: 10px;
        """)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Thêm vào layout
        layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(text_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Tạo hiệu ứng khi di chuột qua
        widget.setStyleSheet("""
            QWidget:hover {
                background-color: #f0f8ff;
                border-radius: 15px;
            }
        """)
        
        # Kết nối sự kiện click
        widget.mousePressEvent = lambda event, cat=label_text: self.category_clicked(cat)
        
        return widget

    def category_clicked(self, category):
        """Xử lý khi click vào nút danh mục"""
        # Hiển thị form tương ứng với danh mục được chọn
        if category == "Earnings":
            self.show_earnings_form()
        elif category == "Spending":
            self.show_spending_form()
        elif category == "Savings":
            self.show_savings_form()

    # Các phương thức để hiển thị form tương ứng
    def show_earnings_form(self):
        """Hiển thị form thu nhập"""
        dialog = EarningsDialog(self)
        result = dialog.exec()
        if result:
            self.refresh_all_tabs()

    def show_spending_form(self):
        """Hiển thị form chi tiêu"""
        dialog = SpendingDialog(self)
        result = dialog.exec()
        if result:
            self.refresh_all_tabs()
        
    def show_savings_form(self):
        """Hiển thị form tiết kiệm"""
        dialog = SavingsDialog(self)
        result = dialog.exec()
        if result:
            self.refresh_all_tabs()

    def calculate_totals(self):
        """Tính tổng thu nhập, chi tiêu và tiết kiệm cho người dùng hiện tại"""
        # Lấy danh sách giao dịch của người dùng
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        user_trans_numbers = [ut.transaction_number for ut in user_transactions 
                            if ut.name == self.user.name]
        
        user_transactions = [t for t in transactions 
                            if t.transaction_number in user_trans_numbers]
        
        # Tính tổng
        total_in = sum(t.amount for t in user_transactions if t.category == "Money In")
        total_out = sum(t.amount for t in user_transactions if t.category == "Money Out")
        total_savings = sum(t.amount for t in user_transactions if t.category == "Savings")
        
        return total_in, total_out, total_savings

    def setup_overview_tab(self):
        """Setup the Overview tab content với các số liệu cập nhật"""
        # Kiểm tra xem đã tạo UI cho overview chưa
        if not hasattr(self, 'overview_initialized'):
            # Chỉ tạo UI lần đầu tiên
            layout = QVBoxLayout(self.overview_content)
            layout.setContentsMargins(30, 30, 30, 30)
            layout.addSpacing(40)  # Đẩy banner xuống một chút

# Banner khung chào
            banner = QFrame()
            banner.setFixedHeight(120)
            banner.setFixedWidth(700)  # Làm khung ngắn lại
            banner.setStyleSheet("""
            background-color: #3e82d3;
            border-radius: 15px;
                            """)

            banner_layout = QVBoxLayout(banner)
            self.banner_title = QLabel(f"Hello, {self.user.name}")
            self.banner_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.banner_title.setStyleSheet("""
             font-size: 28px;
                font-weight: bold;
                color: white;
            """)
            banner_layout.addWidget(self.banner_title)

            layout.addWidget(banner, alignment=Qt.AlignmentFlag.AlignHCenter) 
            
            # Financial info layout with large spacing
            finance_layout = QVBoxLayout()
            finance_layout.setSpacing(1)  # Large spacing between fields
            
            # Money out field with specific styling
            money_out_layout = QHBoxLayout()
            money_out_label = QLabel("Total Expense:")
            money_out_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
            
            self.money_out_value = QLineEdit()
            self.money_out_value.setReadOnly(True)
            self.money_out_value.setFixedSize(450, 60)
            self.money_out_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.money_out_value.setStyleSheet("""
                border: 1px solid #F44336;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 16px;
                color: black;
                background-color: #ffebee;
            """)
            
            money_out_layout.addWidget(money_out_label)
            money_out_layout.addWidget(self.money_out_value)
            money_out_label.setFixedWidth(180)
            # Money in field with light green background
            money_in_layout = QHBoxLayout()
            money_in_label = QLabel("Total Income:")
            money_in_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
            
            self.money_in_value = QLineEdit()
            self.money_in_value.setReadOnly(True)
            self.money_in_value.setFixedSize(450, 60)
            self.money_in_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.money_in_value.setStyleSheet("""
                border: 1px solid #4CAF50;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 16px;
                color: black;
                background-color: #e6ffe6;
            """)
            
            money_in_layout.addWidget(money_in_label)
            money_in_layout.addWidget(self.money_in_value)
            money_in_label.setFixedWidth(180) 

            # Savings field
            savings_layout = QHBoxLayout()
            savings_label = QLabel("Total Savings:")
            savings_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
            
            self.savings_value = QLineEdit()
            self.savings_value.setReadOnly(True)
            self.savings_value.setFixedSize(450, 60)
            self.savings_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.savings_value.setStyleSheet("""
                border: 1px solid #2196F3;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 16px;
                color: black;
                background-color: #e3f2fd;
            """)
            
            savings_layout.addWidget(savings_label)
            savings_layout.addWidget(self.savings_value)
            savings_label.setFixedWidth(180) 

            # Balance field with light yellow background
            balance_layout = QHBoxLayout()
            balance_label = QLabel("Balance:")
            balance_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #8B4513;")  # Brown color
            
            self.balance_value = QLineEdit()
            self.balance_value.setReadOnly(True)
            self.balance_value.setFixedSize(450, 60)
            self.balance_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.balance_value.setStyleSheet("""
                border: 1px solid #FFC107;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 16px;
                color: black;
                background-color: #fff9e6;
            """)
            
            balance_layout.addWidget(balance_label)
            balance_label.setFixedWidth(180) 
            balance_layout.addWidget(self.balance_value)
            
            # Add all financial layouts
            finance_layout.addLayout(money_in_layout)
            finance_layout.addLayout(money_out_layout)
            finance_layout.addLayout(savings_layout)
            finance_layout.addLayout(balance_layout)
            
            # Add financial layout to content
            layout.addLayout(finance_layout)
            layout.addStretch()
            
            # Đánh dấu đã khởi tạo UI
            self.overview_initialized = True
        
        # Cập nhật dữ liệu
        # Calculate totals
        total_in, total_out, total_savings = self.calculate_totals()
        balance = total_in - total_out 
        
        # Cập nhật giá trị các widget
        self.banner_title.setText(f"Hello, {self.user.name}")
        self.money_in_value.setText(f"{total_in:,.0f} VND")
        self.money_out_value.setText(f"{total_out:,.0f} VND")
        self.savings_value.setText(f"{total_savings:,.0f} VND")
        self.balance_value.setText(f"{balance:,.0f} VND")

    def setup_history_tab(self):
        """Setup the History tab content"""
        try:
            # Ensure we check if layout already exists before creating a new one
            layout = None
            if self.history_content.layout() is None:
                # Create a new layout only if there isn't one already
                layout = QVBoxLayout(self.history_content)
                layout.setContentsMargins(0, 0, 0, 0)
            else:
                # Get the existing layout
                layout = self.history_content.layout()
                # Clear the existing layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
            
            # Add the HistoryTab widget
            from money_tracker.ui.history_tab import HistoryTab
            self.history_tab_widget = HistoryTab(self)
            layout.addWidget(self.history_tab_widget)
            
        except Exception as e:
            print(f"Error setting up history tab: {e}")
    
    def setup_management_tab(self):
        """Thiết lập tab Management"""
        try:
            # Explicit layout creation for management_content
            if hasattr(self, 'management_content'):
                # Clear any existing layout
                if self.management_content.layout():
                    # Remove all existing widgets from the layout
                    while self.management_content.layout().count():
                        item = self.management_content.layout().takeAt(0)
                        widget = item.widget()
                        if widget:
                            widget.deleteLater()
                else:
                    # Create layout if it doesn't exist
                    management_layout = QVBoxLayout(self.management_content)
                    management_layout.setContentsMargins(0, 0, 0, 0)
                
                # Now create and add the management tab
                self.management_tab = ManagementTab(self)
                self.management_content.layout().addWidget(self.management_tab)
        except Exception as e:
            print(f"Error setting up management tab: {e}")

    def force_refresh_history_tab(self):
        """Buộc làm mới hoàn toàn tab History"""
        try:
            if hasattr(self, 'history_tab_widget'):
                # Tải lại dữ liệu từ bộ nhớ
                self.transactions = load_transactions()
                self.user_transactions = load_user_transactions()
                
                # Cập nhật dữ liệu cho HistoryTab
                self.history_tab_widget.load_transactions()
                
                # Làm mới giao diện
                self.history_tab_widget.history_table.reset()
                self.history_tab_widget.clear_form()
                
                # Cập nhật lại kích thước bảng nếu cần
                self.history_tab_widget.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.SectionResizeMode.Stretch)
                
                self.history_tab_widget.update()
                self.history_content.update()
            else:
                # Nếu chưa có tab History, thiết lập nó
                self.setup_history_tab()
        except Exception as e:
            print(f"Error force refreshing history tab: {e}")
    def refresh_all_tabs(self):
        self.setup_overview_tab()
        
        if hasattr(self, 'history_tab_widget'):
            self.force_refresh_history_tab()
        
        if hasattr(self, 'management_tab'):
            self.management_tab.refresh_charts()

    def setup_setting_tab(self):
        try:
            if not hasattr(self, 'setting_initialized'):
                layout = QVBoxLayout(self.setting_content)
                layout.setContentsMargins(20, 20, 20, 20)
            
            # Container chính
                container = QWidget()
                container.setStyleSheet("""
                background-color: white;
                border-radius: 40px;
            """)
                container_layout = QVBoxLayout(container)
                container_layout.setContentsMargins(40, 40, 40, 40)
                container_layout.setSpacing(20)
  
                settings_img = QLabel()
                base_dir = os.path.dirname(__file__)
                assets_path = os.path.join(base_dir, "..", "assets", "Settings.png")
                pixmap = QPixmap(os.path.abspath(assets_path))
                if pixmap.isNull():
                    print("⚠️ Không thể load ảnh Settings.png")
                    settings_img.setText("Image not found")
                else:
                    settings_img.setPixmap(pixmap.scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
)

                settings_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

                container_layout.addWidget(settings_img)


            # 👉 Layout chứa các nút
                buttons_layout = QHBoxLayout()
                buttons_layout.setSpacing(30)

                button_style = """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 15px;
                    font-weight: bold;
                    min-width: 130px;
                }
                QPushButton:hover {
                    background-color: #1e88e5;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """

            # Nút
                self.user_guide_btn = QPushButton("User Guide")
                self.logout_btn = QPushButton("Log out")
                self.reset_btn = QPushButton("Reset")
                self.exit_btn = QPushButton("Exit")

                for btn in [self.user_guide_btn, self.logout_btn, self.reset_btn, self.exit_btn]:
                    btn.setStyleSheet(button_style)
                    buttons_layout.addWidget(btn)

            # Gán sự kiện
                self.user_guide_btn.clicked.connect(self.show_user_guide)
                self.logout_btn.clicked.connect(self.logout)
                self.reset_btn.clicked.connect(self.reset_app)
                self.exit_btn.clicked.connect(self.close_app)

            # Thêm layout các nút vào container
                container_layout.addSpacing(10)
                container_layout.addLayout(buttons_layout)

            # Thêm container vào layout chính
                layout.addWidget(container)

                self.setting_initialized = True
        except Exception as e:
            print(f"Error setting up setting tab: {e}")



    # Các phương thức xử lý cho các nút
    def show_user_guide(self):
        """Display user guide in English"""
        self.show_styled_message(
            "User Guide",
            "Welcome to Money Tracker!\n\n"
            "- Overview Tab: View your financial summary\n"
            "- New Transaction Tab: Add new transactions\n"
            "- Management Tab: Manage and analyze your spending\n"
            "- History Tab: View and edit transaction history\n"
            "- Setting Tab: Settings and other options"
        )
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
    def logout(self):
        """Log out from the application"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Logout")
        msg_box.setText("Do you want to logout?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Apply styling
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
        
        confirm = msg_box.exec()
        
        if confirm == QMessageBox.StandardButton.Yes:
            # Close current window
            self.close()
            
            # Show login window
            from money_tracker.ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()

    def reset_app(self):
        """Reset the application to initial state"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Reset")
        msg_box.setText("Are you sure you want to reset the application? All data will be deleted.")
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Apply styling
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
        
        confirm = msg_box.exec()
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Delete all transactions for current user
                all_transactions = load_transactions()
                user_transactions = load_user_transactions()
                
                # Get transaction IDs for current user
                user_trans_numbers = [ut.transaction_number for ut in user_transactions 
                                    if ut.name == self.user.name]
                
                # Filter out transactions not belonging to current user
                transactions_to_keep = [t for t in all_transactions 
                                    if t.transaction_number not in user_trans_numbers]
                
                # Filter out links not belonging to current user
                user_trans_to_keep = [ut for ut in user_transactions 
                                if ut.name != self.user.name]
                
                # Save filtered lists
                save_transactions(transactions_to_keep)
                save_user_transactions(user_trans_to_keep)
                
                # Update application data
                self.transactions = transactions_to_keep
                self.user_transactions = user_trans_to_keep
                
                # Refresh all tabs
                self.refresh_all_tabs()
                
                self.show_styled_message(
                    "Reset Complete",
                    "Application has been reset successfully."
                )
                
            except Exception as e:
                self.show_styled_message(
                    "Reset Error",
                    f"An error occurred while resetting the application: {e}",
                    QMessageBox.Icon.Warning
                )

    def close_app(self):
        """Close the application"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Exit")
        msg_box.setText("Are you sure you want to exit the application?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        # Apply styling
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
        
        confirm = msg_box.exec()
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()