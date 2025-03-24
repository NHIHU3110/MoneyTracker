from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCharts import QChart, QChartView, QPieSeries

from money_tracker.utils.data_handler import load_transactions, load_user_transactions


class ManagementTab(QWidget):
    """Tab Quản lý hiển thị biểu đồ phân phối thu nhập và chi tiêu"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        # Thiết lập layout chính
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        
        # Tạo widget nền trắng
        self.white_background = QFrame()
        self.white_background.setFrameShape(QFrame.Shape.StyledPanel)
        self.white_background.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
        """)
        
        # Layout cho widget nền trắng
        white_bg_layout = QVBoxLayout(self.white_background)
        white_bg_layout.setContentsMargins(20, 20, 20, 20)
        white_bg_layout.setSpacing(20)
        
        # Tạo layout cho các biểu đồ
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(30)
        
        # Layout cho biểu đồ Money In
        money_in_layout = QVBoxLayout()
        money_in_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tiêu đề Money In
        money_in_title = QLabel("Money In Distribution")
        money_in_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        money_in_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        money_in_layout.addWidget(money_in_title)
        
        # Biểu đồ Money In
        self.money_in_chart_view = self.create_money_in_chart()
        money_in_layout.addWidget(self.money_in_chart_view)
        
        # Nút Money In
        self.money_in_button = QPushButton("MONEY IN")
        self.money_in_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.money_in_button.setFixedSize(200, 50)
        self.money_in_button.clicked.connect(self.parent.show_earnings_form)
        money_in_layout.addWidget(self.money_in_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Layout cho biểu đồ Money Out
        money_out_layout = QVBoxLayout()
        money_out_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Tiêu đề Money Out
        money_out_title = QLabel("Money Out Distribution")
        money_out_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        money_out_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        money_out_layout.addWidget(money_out_title)
        
        # Biểu đồ Money Out
        self.money_out_chart_view = self.create_money_out_chart()
        money_out_layout.addWidget(self.money_out_chart_view)
        
        # Nút Money Out
        self.money_out_button = QPushButton("MONEY OUT")
        self.money_out_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.money_out_button.setFixedSize(200, 50)
        self.money_out_button.clicked.connect(self.parent.show_spending_form)
        money_out_layout.addWidget(self.money_out_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Thêm các layout biểu đồ vào layout chung
        charts_layout.addLayout(money_in_layout)
        charts_layout.addLayout(money_out_layout)
        
        # Thêm layout biểu đồ vào layout nền trắng
        white_bg_layout.addLayout(charts_layout)
        
        # Thêm nền trắng vào layout chính
        self.main_layout.addWidget(self.white_background)
    
    def create_money_in_chart(self):
        """Tạo biểu đồ tròn cho phân phối thu nhập"""
        # Lấy dữ liệu giao dịch
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        # Lọc ra các giao dịch của người dùng hiện tại là Money In
        user_transaction_ids = [ut.transaction_number for ut in user_transactions 
                            if ut.name == self.parent.user.name]
        
        user_transactions_data = [t for t in transactions 
                                if t.transaction_number in user_transaction_ids 
                                and t.category == "Money In"]
        
        # Tổng hợp dữ liệu theo category_detail
        category_totals = {}
        for transaction in user_transactions_data:
            # Sử dụng category_detail thay vì amount
            category = transaction.category_detail or "Other"
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
        
        # Tạo series cho biểu đồ tròn
        series = QPieSeries()
        
        # Màu sắc cho các phần
        colors = [
            QColor("#3498db"),   # Blue
            QColor("#f39c12"),   # Orange
            QColor("#2ecc71"),   # Green
            QColor("#e74c3c"),   # Red
            QColor("#9b59b6"),   # Purple
        ]
        
        # Tính tổng số tiền
        total_amount = sum(category_totals.values())
        
        # Nếu không có dữ liệu
        if total_amount == 0:
            slice = series.append("No Data", 1)
            slice.setLabel("No Income")
            slice.setLabelVisible(True)
            slice.setColor(QColor("#cccccc"))
            return self._create_chart_view(series, "Money In")
        
        # Sắp xếp các category theo số tiền giảm dần
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Thêm dữ liệu vào series
        for i, (category, amount) in enumerate(sorted_categories):
            percentage = (amount / total_amount) * 100
            if percentage >= 1:  # Chỉ hiển thị các mục >= 1%
                slice_label = f"{category}\n{percentage:.1f}%"
                slice = series.append(category, amount)
                slice.setLabel(slice_label)
                slice.setLabelVisible(True)
                slice.setColor(colors[i % len(colors)])
        
        return self._create_chart_view(series, "Money In")

    def create_money_out_chart(self):
        """Tạo biểu đồ tròn cho phân phối chi tiêu"""
        # Lấy dữ liệu giao dịch
        transactions = load_transactions()
        user_transactions = load_user_transactions()
        
        # Lọc ra các giao dịch của người dùng hiện tại là Money Out
        user_transaction_ids = [ut.transaction_number for ut in user_transactions 
                            if ut.name == self.parent.user.name]
        
        user_transactions_data = [t for t in transactions 
                                if t.transaction_number in user_transaction_ids 
                                and t.category == "Money Out"]
        
        # Tổng hợp dữ liệu theo category_detail
        category_totals = {}
        for transaction in user_transactions_data:
            # Sử dụng category_detail thay vì amount
            category = transaction.category_detail or "Other"
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
        
        # Tạo series cho biểu đồ tròn
        series = QPieSeries()
        
        # Màu sắc cho các phần
        colors = [
            QColor("#3498db"),   # Blue
            QColor("#f39c12"),   # Orange
            QColor("#2ecc71"),   # Green
            QColor("#e74c3c"),   # Red
            QColor("#9b59b6"),   # Purple
            QColor("#1abc9c"),   # Turquoise
            QColor("#f1c40f")    # Yellow
        ]
        
        # Tính tổng số tiền
        total_amount = sum(category_totals.values())
        
        # Nếu không có dữ liệu
        if total_amount == 0:
            slice = series.append("No Data", 1)
            slice.setLabel("No Expenses")
            slice.setLabelVisible(True)
            slice.setColor(QColor("#cccccc"))
            return self._create_chart_view(series, "Money Out")
        
        # Sắp xếp các category theo số tiền giảm dần
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Thêm dữ liệu vào series
        for i, (category, amount) in enumerate(sorted_categories):
            percentage = (amount / total_amount) * 100
            if percentage >= 1:  # Chỉ hiển thị các mục >= 1%
                slice_label = f"{category}\n{percentage:.1f}%"
                slice = series.append(category, amount)
                slice.setLabel(slice_label)
                slice.setLabelVisible(True)
                slice.setColor(colors[i % len(colors)])
        
        return self._create_chart_view(series, "Money Out")

    def _create_chart_view(self, series, title):
        """Tạo chart view chung cho cả Money In và Money Out"""
        # Tạo biểu đồ
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setTitleFont(QFont("Arial", 12, QFont.Weight.Bold))
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Điều chỉnh chú thích
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # Tạo chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setMinimumSize(300, 300)
        
        return chart_view
    
    def refresh_charts(self):
        """Làm mới các biểu đồ"""
        # Xóa các biểu đồ cũ
        if self.money_in_chart_view:
            self.money_in_chart_view.deleteLater()
        if self.money_out_chart_view:
            self.money_out_chart_view.deleteLater()
        
        # Tạo biểu đồ mới
        self.money_in_chart_view = self.create_money_in_chart()
        self.money_out_chart_view = self.create_money_out_chart()
        
        # Cập nhật layout
        # Tìm vị trí của các biểu đồ trong layout
        charts_layout = self.white_background.layout().itemAt(0).layout()
        
        # Cập nhật biểu đồ Money In
        money_in_layout = charts_layout.itemAt(0).layout()
        money_in_layout.insertWidget(1, self.money_in_chart_view)
        
        # Cập nhật biểu đồ Money Out
        money_out_layout = charts_layout.itemAt(1).layout()
        money_out_layout.insertWidget(1, self.money_out_chart_view)


    # Phương thức để thêm vào MainWindow
    def setup_management_tab(self):
        """Thiết lập tab Management"""
        try:
            # Check that we have the management_content widget
            if not hasattr(self, 'management_content'):
                print("Warning: management_content not found in MainWindow")
                return
                
            # Create layout for the management content if needed
            if self.management_content.layout() is None:
                management_layout = QVBoxLayout(self.management_content)
                management_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create the management tab widget
            self.management_tab = ManagementTab(self)
            self.management_content.layout().addWidget(self.management_tab)
            
            # Connect the tab changed signal if possible
            if hasattr(self, 'tab_widget'):
                # Disconnect first to avoid duplicate connections
                try:
                    self.tab_widget.currentChanged.disconnect(self.refresh_management_tab)
                except:
                    pass  # Ignore if not connected yet
                self.tab_widget.currentChanged.connect(self.refresh_management_tab)
        except Exception as e:
            print(f"Error setting up management tab: {e}")

    # Phương thức để làm mới tab Management
    def refresh_management_tab(self, index):
        """Làm mới tab Management khi người dùng chuyển đến tab này"""
        try:
            if hasattr(self, 'management_tab') and index == 2:  # Assuming Management is at index 2
                self.management_tab.refresh_charts()
        except Exception as e:
            print(f"Error refreshing management tab: {e}")