import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QFormLayout, QMessageBox,
    QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from money_tracker.utils.data_handler import *
class HistoryTab(QWidget):
    """History Tab implementation matching the reference design with requested adjustments"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_filter = None  
        self.init_ui()
        self.load_transactions()

    def init_ui(self):
        # Main layout without margins to remove extra white space
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # White background widget with rounded corners
        white_background = QFrame()
        white_background.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)
        
        # Layout for the white background
        bg_layout = QVBoxLayout(white_background)
        bg_layout.setContentsMargins(20, 20, 20, 20)
        bg_layout.setSpacing(20)
        
        # Two-column layout for main content
        content_layout = QHBoxLayout()
        
        # Left side: Transaction table
        left_layout = QVBoxLayout()
        
        # Create table with 4 columns
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["No", "Date", "Category", "Amount"])

        # Set column widths
        header = self.history_table.horizontalHeader()

        #header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        self.history_table.verticalHeader().setDefaultSectionSize(40)
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: white;
                padding: 5px;
                border-bottom: 1px solid #d3d3d3;
                border-right: 0px solid #d3d3d3;
                font-weight: bold;
                color: black;
                min-height: 40px; 
            }
        """)
        # Set initial column widths
        self.history_table.setColumnWidth(0, 50)
        self.history_table.setColumnWidth(1, 100)
        self.history_table.setColumnWidth(2, 100)
        self.history_table.setColumnWidth(3, 100)
        
        # Set table properties
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #d3d3d3;
            }
            QHeaderView::section {
                background-color: white;
                padding: 5px;
                border-bottom: 1px solid #d3d3d3;
                border-right: 1px solid #d3d3d3;
                font-weight: bold;
                color: black;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #d3d3d3;
                color: black;
            }
        """)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(True)
        
        # Connect selection change event
        self.history_table.selectionModel().selectionChanged.connect(self.on_row_selected)
        
        # Add table to left layout
        left_layout.addWidget(self.history_table)
        
        # Right side: Form fields
        right_layout = QFormLayout()
        right_layout.setContentsMargins(10, 0, 0, 0)
        right_layout.setVerticalSpacing(20)
        
        # No. field - blue border
        self.no_input = QLineEdit()
        self.no_input.setReadOnly(True)
        self.no_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #3498db;
                border-radius: 5px;
                padding: 8px;
                min-height: 20px;
                color: black;
            }
        """)
        no_label = QLabel("No. :")
        no_label.setStyleSheet("font-size: 14px; color: black;")
        right_layout.addRow(no_label, self.no_input)
        
        # Date field - green border
        self.date_input = QLineEdit()
        self.date_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2ecc71;
                border-radius: 5px;
                padding: 8px;
                min-height: 20px;
                color: black;
            }
        """)
        date_label = QLabel("Date:")
        date_label.setStyleSheet("font-size: 14px; color: black;")
        right_layout.addRow(date_label, self.date_input)
        
        # Amount field - orange border
        self.amount_input = QLineEdit()
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #f39c12;
                border-radius: 5px;
                padding: 8px;
                min-height: 20px;
                color: black;
            }
        """)
        amount_label = QLabel("Amount:")
        amount_label.setStyleSheet("font-size: 14px; color: black;")
        right_layout.addRow(amount_label, self.amount_input)
        

        # Lưu giá trị category dưới dạng biến
        self.selected_category = ""
        
        
        # Add layouts to content layout
        content_layout.addLayout(left_layout, 3)  # Left side takes more space
        content_layout.addLayout(right_layout, 2)  # Right side takes less space
        
        # Add content layout to background layout
        bg_layout.addLayout(content_layout)
        
        # Action buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Create buttons with same styling
        self.money_in_btn = QPushButton("Money in")
        self.money_out_btn = QPushButton("Money out")
        self.clear_btn = QPushButton("Clear")
        self.delete_btn = QPushButton("Delete")
        self.save_btn = QPushButton("Save")
        self.show_all_btn = QPushButton("Show All")  # Thêm nút Show All
        
        # Connect button actions
        self.money_in_btn.clicked.connect(self.on_money_in_clicked)
        self.money_out_btn.clicked.connect(self.on_money_out_clicked)
        self.clear_btn.clicked.connect(self.clear_form)
        self.delete_btn.clicked.connect(self.delete_transaction)
        self.save_btn.clicked.connect(self.save_transaction)
        self.show_all_btn.clicked.connect(self.show_all_transactions)  # Kết nối hành động cho nút Show All
        
        # Set button style
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 20px;
                padding: 10px 0px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        self.money_in_btn.setStyleSheet(button_style)
        self.money_out_btn.setStyleSheet(button_style)
        self.clear_btn.setStyleSheet(button_style)
        self.delete_btn.setStyleSheet(button_style)
        self.save_btn.setStyleSheet(button_style)
        self.show_all_btn.setStyleSheet(button_style)
        
        # Add buttons to layout
        buttons_layout.addWidget(self.money_in_btn)
        buttons_layout.addWidget(self.money_out_btn)
        buttons_layout.addWidget(self.show_all_btn)  # Thêm nút Show All vào layout
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.save_btn)
        
        # Add buttons layout to background layout
        bg_layout.addLayout(buttons_layout)
        
        # Add the white background to main layout
        main_layout.addWidget(white_background)
        
        # Set the style for the main widget to remove extra white space
        self.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
    
    def load_transactions(self, filter_category=None):
        """Load user's transactions from data storage with optional filtering"""
        try:
            self.history_table.setRowCount(0)
            self.current_filter = filter_category  # Lưu bộ lọc hiện tại
            
            if not hasattr(self.parent, 'user') or not hasattr(self.parent, 'transactions'):
                return
                    
            # Get all transactions and filter by user
            all_transactions = self.parent.transactions
            user_transactions_links = self.parent.user_transactions
            
            # Get transaction IDs for current user
            user_trans_numbers = [ut.transaction_number for ut in user_transactions_links 
                                if ut.name == self.parent.user.name]
            
            # Get actual transactions that belong to the user
            user_transactions = [t for t in all_transactions 
                            if t.transaction_number in user_trans_numbers]
            
            # Apply category filter if specified
            if filter_category:
                if filter_category == "Money In":
                    # Include Money In, Salary, Allowance
                    user_transactions = [t for t in user_transactions 
                                    if t.category == "Money In" or 
                                    (hasattr(t, "category_detail") and 
                                    t.category == "Money In" and 
                                    t.category_detail in ["Salary", "Allowance"])]
                elif filter_category == "Money Out":
                    user_transactions = [t for t in user_transactions if t.category == "Money Out" or
                                        (hasattr(t, "category_detail") and 
                                         t.category == "Money Out" and
                                         t.category_detail in ["Food and drink", "Moving", "Shopping", "Invoice"])]
            
            # Sort transactions by date (newest first)
            sorted_transactions = sorted(
                user_transactions, 
                key=lambda x: x.transaction_date if isinstance(x.transaction_date, str) else str(x.transaction_date),
                reverse=True
            )


            # Add row numbers
            for i, transaction in enumerate(sorted_transactions):
                row_position = self.history_table.rowCount()
                self.history_table.insertRow(row_position)
                
                # Format date as string
                date_str = transaction.transaction_date
                if isinstance(date_str, (datetime.date, datetime.datetime)):
                    date_str = date_str.strftime('%Y-%m-%d')
                
                # Display sequential number but store actual transaction_number
                seq_number_item = QTableWidgetItem(str(i + 1))
                seq_number_item.setData(Qt.ItemDataRole.UserRole, str(transaction.transaction_number))
                self.history_table.setItem(row_position, 0, seq_number_item)
                
                self.history_table.setItem(row_position, 1, QTableWidgetItem(str(date_str)))
            
                # Get category - using category_detail if available for better display
                category = transaction.category
                if hasattr(transaction, 'category_detail') and transaction.category_detail:
                    if category == "Money In" and transaction.category_detail in ["Salary", "Allowance"]:
                        category = transaction.category_detail
                    if category == "Money Out" and transaction.category_detail in ["Food and drink", "Moving", "Shopping", "Invoice"]:
                        category = transaction.category_detail
                # Category item with black text
                category_item = QTableWidgetItem(category)
                category_item.setForeground(QColor(0, 0, 0))  # Force black text
                self.history_table.setItem(row_position, 2, category_item)
                
                # Format amount with currency
                amount_item = QTableWidgetItem(f"{float(transaction.amount):,.0f} VND")
                
                # Color code based on category
                if category == "Money In" or category == "Salary" or category == "Allowance":
                    amount_item.setForeground(QColor(0, 128, 0))  # Green for income
                else:  # Money Out
                    amount_item.setForeground(QColor(255, 0, 0))  # Red for expenses
                    
                self.history_table.setItem(row_position, 3, amount_item)
            # self.history_table.update()
            # self.update()
        except Exception as e:
            print(f"Error loading transactions in history tab: {e}")
    
    def on_row_selected(self):
        """Handle row selection in the table"""
        selected_indexes = self.history_table.selectedIndexes()
        if not selected_indexes:
            return
            
        row = selected_indexes[0].row()
        
        # Get data from selected row
        transaction_id = self.history_table.item(row, 0).data(Qt.ItemDataRole.UserRole) if hasattr(self.history_table.item(row, 0), 'data') else self.history_table.item(row, 0).text()
        date = self.history_table.item(row, 1).text()
        category = self.history_table.item(row, 2).text()
        amount = self.history_table.item(row, 3).text()
        
        # Clean amount value (remove VND and commas)
        amount = amount.replace(" VND", "").replace(",", "")
        
        # Fill form fields
        self.no_input.setText(transaction_id)
        self.date_input.setText(date)
        self.amount_input.setText(amount)
        
        # Lưu category vào biến nhưng không hiển thị
        self.selected_category = category

    def clear_form(self):
        """Clear form fields"""
        self.no_input.clear()
        self.date_input.clear()
        self.amount_input.clear()
        self.selected_category = ""
        self.history_table.clearSelection()

    def on_money_in_clicked(self):
        """Filter by Money In transactions and set category to Money In"""
        # Lưu category vào biến
        self.selected_category = "Money In"
        
        # Lọc bảng hiển thị
        self.load_transactions(filter_category="Money In")

    def on_money_out_clicked(self):
        """Filter by Money Out transactions and set category to Money Out"""
        # Lưu category vào biến
        self.selected_category = "Money Out"
        
        # Lọc bảng hiển thị
        self.load_transactions(filter_category="Money Out")
    
    def delete_transaction(self):
        """Delete selected transaction"""
        from money_tracker.utils import load_transactions, save_transactions, load_user_transactions, save_user_transactions
        
        selected_indexes = self.history_table.selectedIndexes()
        if not selected_indexes:
            self.show_styled_message(
                "No Selection", 
                "Please select a transaction to delete.",
                QMessageBox.Icon.Warning
            )
            return
            
        row = selected_indexes[0].row()
        transaction_id = self.history_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Show confirmation dialog
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Delete")
        msg_box.setText("Are you sure you want to delete this transaction?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
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
        
        confirm = msg_box.exec()
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Get all transactions
                all_transactions = load_transactions()
                user_transactions = load_user_transactions()
                
                # Find and remove the transaction
                transactions_to_keep = [t for t in all_transactions if 
                                    t.transaction_number != transaction_id]
                
                # Remove from user transactions links too
                user_trans_to_keep = [ut for ut in user_transactions if 
                                ut.transaction_number != transaction_id]
                
                # Save updated lists
                save_transactions(transactions_to_keep)
                save_user_transactions(user_trans_to_keep)
                
                # Update parent's transactions
                self.parent.transactions = transactions_to_keep
                self.parent.user_transactions = user_trans_to_keep
                
                # Refresh display
                self.load_transactions()
                self.clear_form()
                
                # Notify parent to refresh
                if hasattr(self.parent, 'setup_overview_tab'):
                    self.parent.setup_overview_tab()
                
                self.show_styled_message(
                    "Success", 
                    "Transaction deleted successfully",
                    QMessageBox.Icon.Information
                )
                
            except Exception as e:
                self.show_styled_message(
                    "Error", 
                    f"Failed to delete transaction: {e}",
                    QMessageBox.Icon.Warning
                )

    
    def save_transaction(self):
        """Save transaction changes"""
        from money_tracker.utils import load_transactions, save_transactions
        
        # Get data from form
        transaction_id = self.no_input.text()
        date_str = self.date_input.text()
        amount_str = self.amount_input.text()
        
        if not transaction_id:
            self.show_styled_message(
                "No Transaction Selected", 
                "Please select a transaction to edit.",
                QMessageBox.Icon.Warning
            )
            return
            
        if not date_str or not amount_str:
            self.show_styled_message(
                "Missing Information", 
                "Please fill in date and amount fields.",
                QMessageBox.Icon.Warning
            )
            return
            
        try:
            # Parse date and amount
            try:
                # Validate date format
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                # Keep date as string for compatibility
                date = date_str
            except ValueError:
                self.show_styled_message(
                    "Invalid Date", 
                    "Please enter date in YYYY-MM-DD format",
                    QMessageBox.Icon.Warning
                )
                return
                
            try:
                amount = float(amount_str)
            except ValueError:
                self.show_styled_message(
                    "Invalid Amount", 
                    "Please enter a valid number for amount",
                    QMessageBox.Icon.Warning
                )
                return
            
            # Get category
            if not self.selected_category:
                self.show_styled_message(
                    "Missing Category", 
                    "Please select a category by clicking 'Money In' or 'Money Out' button",
                    QMessageBox.Icon.Warning
                )
                return
            
            category = self.selected_category
            
            # Load all transactions
            all_transactions = load_transactions()
            
            # Find the transaction to update
            transaction_found = False
            for transaction in all_transactions:
                if transaction.transaction_number == transaction_id:
                    # Update transaction fields
                    transaction.transaction_date = date
                    transaction.category = category
                    transaction.amount = amount
                    # Preserve category_detail if it exists
                    if not hasattr(transaction, 'category_detail'):
                        transaction.category_detail = ""
                    transaction_found = True
                    break
            
            if not transaction_found:
                self.show_styled_message(
                    "Transaction Not Found", 
                    "The selected transaction could not be found.",
                    QMessageBox.Icon.Warning
                )
                return
            
            # Save updated transactions
            save_transactions(all_transactions)
            
            # Update parent's transactions
            self.parent.transactions = all_transactions
            
            # Refresh display
            self.load_transactions()
            self.clear_form()
            
            # Notify parent to refresh
            if hasattr(self.parent, 'setup_overview_tab'):
                self.parent.setup_overview_tab()
            
            self.show_styled_message(
                "Success", 
                "Transaction updated successfully",
                QMessageBox.Icon.Information
            )
            
        except Exception as e:
            self.show_styled_message(
                "Error", 
                f"Failed to update transaction: {e}",
                QMessageBox.Icon.Warning
            )

    def show_all_transactions(self):
        """Reset filter and show all transactions"""
        self.load_transactions(filter_category=None)
        self.setWindowTitle("Transaction History - All Transactions")
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