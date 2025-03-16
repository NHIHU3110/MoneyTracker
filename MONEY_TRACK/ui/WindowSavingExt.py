import logging
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QDate
from MONEY_TRACK.libs.DataConnector import DataConnector
from MONEY_TRACK.models.Transaction import Transaction
from MONEY_TRACK.models.MTuser_Transaction import MTuser_Transaction
from MONEY_TRACK.ui.WindowSaving import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WindowSavingExt(Ui_MainWindow):
    def setupUi(self, MainWindow, main_ui):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.main_ui = main_ui
        self.setupSignalAndSlot()
        self.set_default_date()

    def set_default_date(self):
        today = QDate.currentDate()
        self.dateEdit.setDate(today)

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButtonSave.clicked.connect(self.save_transaction)
        self.pushButtonClose.clicked.connect(self.close_window)
        self.pushButtonClear.clicked.connect(self.clear_fields)

    def close_window(self):
        reply = QMessageBox.question(self.MainWindow, 'Confirm Close', 'Are you sure you want to close the window?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.MainWindow.close()

    def clear_fields(self):
        self.lineEditAmount.clear()
        self.dateEdit.setDate(QDate.currentDate())

    def generate_transaction_no(self):
        dc = DataConnector()
        mtuser_transactions = dc.get_all_mtuser_transactions()
        user_transactions = [ut for ut in mtuser_transactions if ut.Name == self.main_ui.user_name]
        new_no = str(len(user_transactions) + 1)
        return new_no

    def update_transactions(self, new_transaction):
        dc = DataConnector()
        transactions = dc.get_all_transactions()
        transactions.append(new_transaction)
        transactions.sort(key=lambda x: x.TransactionDate)

        mtuser_transactions = dc.get_all_mtuser_transactions()
        user_transactions = [tr for tr in transactions if any(
            ut.Name == self.main_ui.user_name and ut.TransactionID == tr.TransactionNo for ut in mtuser_transactions)]

        for index, transaction in enumerate(user_transactions):
            transaction.TransactionNo = str(index + 1)

        dc.update_transactions(transactions)
        self.main_ui.load_transactions_for_user()

    def save_transaction(self):
        logging.debug("Save transaction started.")
        amount_str = self.lineEditAmount.text().strip()
        date = self.dateEdit.text().strip()
        category = "Savings"
        category_detail = "Savings"
        if not amount_str or not date:
            QMessageBox.warning(self.MainWindow, "Error", "Please fill in all fields!")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            QMessageBox.warning(self.MainWindow, "Error", "Invalid amount. Please enter a numerical value.")
            return
        new_transaction_no = self.generate_transaction_no()
        new_transaction = Transaction(new_transaction_no, date, amount, category, category_detail)
        self.update_transactions(new_transaction)
        self.link_transaction_to_user(new_transaction_no)
        self.main_ui.show_pie_chart()  # Update the pie chart for Savings
        self.main_ui.show_pie_chart_money_out()  # Update the pie chart for Money Out
        QMessageBox.information(self.MainWindow, "Success", "Transaction saved successfully!")

    def link_transaction_to_user(self, transaction_no):
        dc = DataConnector()
        mtuser_transactions = dc.get_all_mtuser_transactions()
        new_link = MTuser_Transaction(self.main_ui.user_name, transaction_no, "Savings")
        mtuser_transactions.append(new_link)
        dc.update_mtuser_transactions(mtuser_transactions)