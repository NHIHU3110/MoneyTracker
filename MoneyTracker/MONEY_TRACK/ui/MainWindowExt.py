# MONEY_TRACK/ui/MainWindowExt.py
import io

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QAbstractItemView
from matplotlib import pyplot as plt

from MoneyTracker.MONEY_TRACK.libs.DataConnector import DataConnector
import logging

from MoneyTracker.MONEY_TRACK.models.Transaction import Transaction
from MoneyTracker.MONEY_TRACK.ui.MainWindow import Ui_MainWindow

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindowExt(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.data_connector = DataConnector()
        self.user_name = None
        # Used to track the transaction being edited
        self.original_transaction_no = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
        self.setupTableWidget()

    def setupTableWidget(self):
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Transaction No", "Date", "Category", "Category Detail", "Amount"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(Qt.PenStyle.SolidLine)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)



    def load_transactions_for_user(self, category_filter=None):
        try:
            mtuser_transactions = self.data_connector.get_all_mtuser_transactions()
            all_transactions = self.data_connector.get_all_transactions()

            # Filter transactions by user
            user_transactions_ids = [
                ut.TransactionID for ut in mtuser_transactions if ut.Name == self.user_name
            ]

            user_transactions = [
                tr for tr in all_transactions if tr.TransactionNo in user_transactions_ids
            ]

            # Apply category filter if needed
            if category_filter:
                user_transactions = [tr for tr in user_transactions if tr.Category == category_filter]

            # Filter out transactions from 02/28/2025
            user_transactions = [tr for tr in user_transactions if tr.TransactionDate != '02/28/2025']

            # Sort transactions by TransactionNo
            user_transactions.sort(key=lambda tr: tr.TransactionNo)

            self.tableWidget.setRowCount(0)
            row_index = 0
            for transaction in user_transactions:
                self.tableWidget.insertRow(row_index)
                self.tableWidget.setItem(row_index, 0, QTableWidgetItem(transaction.TransactionNo))
                self.tableWidget.setItem(row_index, 1, QTableWidgetItem(transaction.TransactionDate))
                self.tableWidget.setItem(row_index, 2, QTableWidgetItem(transaction.Category))
                self.tableWidget.setItem(row_index, 3, QTableWidgetItem(transaction.CategoryDetail))
                self.tableWidget.setItem(row_index, 4, QTableWidgetItem(str(transaction.Amount)))
                row_index += 1

            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            logging.error(f"Error loading transactions: {e}")

    def setupSignalAndSlot(self):
        self.pushButtonClose.clicked.connect(self.process_close)
        self.tableWidget.itemSelectionChanged.connect(self.display_transaction_details)
        self.pushButtonClear.clicked.connect(self.clear_transaction_details)
        self.pushButtonDelete.clicked.connect(self.delete_transaction)
        self.pushButtonSave.clicked.connect(self.save_transaction)
        self.pushButtonMoneyIn.clicked.connect(lambda: self.filter_transactions("Money In"))
        self.pushButtonMoneyOut.clicked.connect(lambda: self.filter_transactions("Money Out"))
        self.pushButtonLogOut.clicked.connect(self.process_logout)
        self.pushButtonSavings_2.clicked.connect(lambda: self.filter_transactions("Savings"))
        self.pushButtonEarnings.clicked.connect(self.open_earnings_window)
        self.pushButtonSpending.clicked.connect(self.open_spending_window)
        self.pushButtonSavings.clicked.connect(self.open_savings_window)

    def show_pie_chart(self, name):
        try:
            transactions = self.data_connector.get_transactions_by_name(name)

            if not transactions:
                logging.error(f"No transactions found for user '{name}'.")
                self.labelMoneyIn.clear()  # Có thể thay labelMoneyIn nếu muốn hiển thị ở một label khác
                return

            # Xử lý cho Money In
            money_in_transactions = [tr for tr in transactions if tr.Category == "Money In"]

            if not money_in_transactions:
                logging.warning(f"No 'Money In' transactions found for user '{name}'.")
                self.labelMoneyIn.clear()  # Dùng labelMoneyIn cho cả 2 loại
            else:
                category_details_in = {}
                for tr in money_in_transactions:
                    if tr.CategoryDetail in category_details_in:
                        category_details_in[tr.CategoryDetail] += float(tr.Amount)
                    else:
                        category_details_in[tr.CategoryDetail] = float(tr.Amount)

                if category_details_in:
                    labels_in = list(category_details_in.keys())
                    sizes_in = list(category_details_in.values())

                    # Define custom colors
                    colors_in = ['#4e73df', '#f5b9c9', '#f1c40f', '#9b59b6', '#1f77b4']  # Add more colors if needed

                    fig, ax = plt.subplots(figsize=(3, 3))  # Adjust the size of the pie chart here (smaller size)
                    ax.pie(sizes_in, labels=labels_in, startangle=30, colors=colors_in, textprops={'fontsize': 4})
                    ax.axis('equal')  # Đảm bảo biểu đồ tròn

                    # Add legend for each segment, placed to the right of the chart
                    ax.legend(labels_in, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))

                    # Adjust layout to fit everything into the view
                    fig.tight_layout(pad=1.0)  # Ensure tight layout to avoid overflow

                    # Resize to fit the label area
                    width, height = self.labelMoneyIn.width(), self.labelMoneyIn.height()
                    fig.set_size_inches(width / fig.dpi, height / fig.dpi)

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    pixmap = QPixmap()
                    pixmap.loadFromData(buf.getvalue())
                    self.labelMoneyIn.setPixmap(pixmap)
                    buf.close()

            # Xử lý cho Money Out
            money_out_transactions = [tr for tr in transactions if tr.Category == "Money Out"]

            if not money_out_transactions:
                logging.warning(f"No 'Money Out' transactions found for user '{name}'.")
                self.labelMoneyOut.clear()  # Dùng labelMoneyOut cho Money Out
            else:
                category_details_out = {}
                for tr in money_out_transactions:
                    if tr.CategoryDetail in category_details_out:
                        category_details_out[tr.CategoryDetail] += float(tr.Amount)
                    else:
                        category_details_out[tr.CategoryDetail] = float(tr.Amount)

                if category_details_out:
                    labels_out = list(category_details_out.keys())
                    sizes_out = list(category_details_out.values())

                    # Define custom colors for Money Out
                    colors_out = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']  # Add more colors if needed

                    fig, ax = plt.subplots(figsize=(3, 3))  # Adjust the size of the pie chart here (smaller size)
                    ax.pie(sizes_out, labels=labels_out, startangle=30, colors=colors_out, textprops={'fontsize': 4})
                    ax.axis('equal')  # Đảm bảo biểu đồ tròn

                    # Add legend for each segment, placed to the right of the chart
                    ax.legend(labels_out, title="Categories", loc="center left", bbox_to_anchor=(1, 0.5))

                    # Adjust layout to fit everything into the view
                    fig.tight_layout(pad=1.0)  # Ensure tight layout to avoid overflow

                    # Resize to fit the label area
                    width, height = self.labelMoneyOut.width(), self.labelMoneyOut.height()
                    fig.set_size_inches(width / fig.dpi, height / fig.dpi)

                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    pixmap = QPixmap()
                    pixmap.loadFromData(buf.getvalue())
                    self.labelMoneyOut.setPixmap(pixmap)
                    buf.close()

        except Exception as e:
            logging.error(f"Error generating pie chart: {e}")



    def showWindow(self, username, password):
        user = self.data_connector.login(username, password)
        if user:
            self.user_name = user.Name
            self.load_transactions_for_user()
            self.update_totals()
            self.lineEditWelcome.setText(f"Hello, {self.user_name}")
            self.show_pie_chart(self.user_name)
            self.MainWindow.show()
        else:
            QMessageBox.warning(
                self.MainWindow,
                "Login Failed",
                "Incorrect username or password."
            )
    def update_totals(self):
        try:
            mtuser_transactions = self.data_connector.get_all_mtuser_transactions()
            transactions = self.data_connector.get_all_transactions()

            total_in = sum(
                float(tr.Amount) for tr in transactions
                if tr.Category == "Money In" and any(
                    ut.Name == self.user_name and ut.TransactionID == tr.TransactionNo for ut in mtuser_transactions)
            )
            total_out = sum(
                float(tr.Amount) for tr in transactions
                if tr.Category == "Money Out" and any(
                    ut.Name == self.user_name and ut.TransactionID == tr.TransactionNo for ut in mtuser_transactions)
            )
            total_savings = sum(
                float(tr.Amount) for tr in transactions
                if tr.Category == "Savings" and any(
                    ut.Name == self.user_name and ut.TransactionID == tr.TransactionNo for ut in mtuser_transactions)
            )

            total_balance = total_in - total_out

            self.lineEditTotalMoneyIn.setText(str(total_in))
            self.lineEditTotalMoneyOut.setText(str(total_out))
            self.lineEditTotalBalance.setText(str(total_balance))
            self.lineEditTotalSavings.setText(str(total_savings))
        except Exception as e:
            logging.error(f"Failed to update totals: {e}")

    def process_logout(self):
        from MoneyTracker.MONEY_TRACK.ui.WindowLoginExt import WindowLoginExt
        confirmation = QMessageBox.question(
            self.MainWindow,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()
            self.login_window = QMainWindow()
            self.login_ui = WindowLoginExt()
            self.login_ui.setupUi(self.login_window)
            self.login_ui.showWindow()

    def process_close(self):
        confirmation = QMessageBox.question(
            self.MainWindow,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()

    def display_transaction_details(self):
        selected_items = self.tableWidget.selectedItems()
        if not selected_items:
            return

        try:
            row = selected_items[0].row()
            transaction_no = self.tableWidget.item(row, 0).text()
            transaction_date = self.tableWidget.item(row, 1).text()
            transaction_category = self.tableWidget.item(row, 2).text()
            transaction_category_detail = self.tableWidget.item(row, 3).text()
            transaction_amount = self.tableWidget.item(row, 4).text()

            self.lineEditNo.setText(transaction_no)
            self.lineEditDate.setText(transaction_date)
            self.lineEditAmount.setText(transaction_amount)

            if transaction_category.lower() == "money in":
                self.radioButtonMoneyIn.setChecked(True)
            else:
                self.radioButtonMoneyOut.setChecked(True)

            # Store original transaction number for further update
            self.original_transaction_no = transaction_no
        except Exception as e:
            logging.error(f"Error displaying transaction details: {e}")

    def clear_transaction_details(self):
        self.lineEditNo.clear()
        self.lineEditDate.clear()
        self.lineEditAmount.clear()
        self.radioButtonMoneyIn.setAutoExclusive(False)
        self.radioButtonMoneyOut.setAutoExclusive(False)
        self.radioButtonMoneyIn.setChecked(False)
        self.radioButtonMoneyOut.setChecked(False)
        self.radioButtonMoneyIn.setAutoExclusive(True)
        self.radioButtonMoneyOut.setAutoExclusive(True)
        self.original_transaction_no = None

    def delete_transaction(self):
        try:
            no = self.lineEditNo.text()
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Confirm Delete")
            dlg.setText(f"Are you sure you want to delete transaction [{no}]?")
            dlg.setIcon(QMessageBox.Icon.Question)
            buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            dlg.setStandardButtons(buttons)
            button = dlg.exec()
            if button == QMessageBox.StandardButton.No:
                return

            transactions = self.data_connector.get_all_transactions()
            transaction_to_remove = next((t for t in transactions if t.TransactionNo == no), None)

            if transaction_to_remove:
                transactions.remove(transaction_to_remove)
                self.data_connector.update_transactions(transactions)
                # Reload transactions (which includes sorting) after deletion.
                self.load_transactions_for_user()
        except Exception as e:
            logging.error(f"Error deleting transaction: {e}")

    # MONEY_TRACK/ui/MainWindowExt.py

    def save_transaction(self):
        try:
            # Retrieve updated values from UI
            new_no = self.lineEditNo.text()
            new_date = self.lineEditDate.text()
            new_amount = float(self.lineEditAmount.text())  # Convert to float instead of int
            new_category = "Money In" if self.radioButtonMoneyIn.isChecked() else "Money Out"

            transactions = self.data_connector.get_all_transactions()
            found = False

            # Find the transaction with the original TransactionNo and update its values
            for t in transactions:
                if t.TransactionNo == self.original_transaction_no:
                    t.TransactionNo = new_no
                    t.TransactionDate = new_date
                    t.Amount = new_amount
                    t.Category = new_category
                    found = True
                    break

            if not found:
                new_transaction = Transaction(new_no, new_date, new_amount, new_category, "")
                transactions.append(new_transaction)
            self.data_connector.update_transactions(transactions)
            self.load_transactions_for_user()  # Reload to reflect changes
            QMessageBox.information(self.MainWindow, "Info", "Transaction saved successfully.")
        except Exception as e:
            logging.error(f"Error saving transaction: {e}")
    def filter_transactions(self, category):
        self.load_transactions_for_user(category_filter=category)

    def open_savings_window(self):
        from MoneyTracker.MONEY_TRACK.ui.WindowSavingExt import WindowSavingExt
        self.savings_window = QMainWindow()
        self.savings_ui = WindowSavingExt()
        self.savings_ui.setupUi(self.savings_window, self)
        self.savings_ui.showWindow()

    def open_earnings_window(self):
        from MoneyTracker.MONEY_TRACK.ui.WindowEarningExt import WindowEarningExt
        self.earnings_window = QMainWindow()
        self.earnings_ui = WindowEarningExt()
        self.earnings_ui.setupUi(self.earnings_window, self)
        self.earnings_ui.showWindow()

    def open_spending_window(self):
        from MoneyTracker.MONEY_TRACK.ui.WindowSpendingExt import WindowSpendingExt
        self.spending_window = QMainWindow()
        self.spending_ui = WindowSpendingExt()
        self.spending_ui.setupUi(self.spending_window, self)
        self.spending_ui.showWindow()