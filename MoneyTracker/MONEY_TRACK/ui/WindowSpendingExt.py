# MONEY_TRACK/ui/WindowSpendingExt.py
import logging
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate
from MoneyTracker.MONEY_TRACK.libs.DataConnector import DataConnector
from MoneyTracker.MONEY_TRACK.models.MTuser_Transaction import MTuser_Transaction
from MoneyTracker.MONEY_TRACK.models.Transaction import Transaction
from MoneyTracker.MONEY_TRACK.ui.WindowSpending import Ui_MainWindow

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WindowSpendingExt(Ui_MainWindow):
    def setupUi(self, MainWindow, main_ui):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.main_ui = main_ui  # Store the reference to MainWindowExt
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
        self.radioButtonFoodDrink.setAutoExclusive(False)
        self.radioButtonMoving.setAutoExclusive(False)
        self.radioButtonShopping.setAutoExclusive(False)
        self.radioButtonInvoice.setAutoExclusive(False)
        self.radioButtonOthers.setAutoExclusive(False)
        self.radioButtonFoodDrink.setChecked(False)
        self.radioButtonMoving.setChecked(False)
        self.radioButtonShopping.setChecked(False)
        self.radioButtonInvoice.setChecked(False)
        self.radioButtonOthers.setChecked(False)
        self.radioButtonFoodDrink.setAutoExclusive(True)
        self.radioButtonMoving.setAutoExclusive(True)
        self.radioButtonShopping.setAutoExclusive(True)
        self.radioButtonInvoice.setAutoExclusive(True)
        self.radioButtonOthers.setAutoExclusive(True)

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
        category = "Money Out"
        category_detail = None
        if self.radioButtonFoodDrink.isChecked():
            category_detail = "FoodDrink"
        elif self.radioButtonMoving.isChecked():
            category_detail = "Moving"
        elif self.radioButtonShopping.isChecked():
            category_detail = "Shopping"
        elif self.radioButtonInvoice.isChecked():
            category_detail = "Invoice"
        elif self.radioButtonOthers.isChecked():
            category_detail = "Others"
        if not amount_str or not date or not category_detail:
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
        QMessageBox.information(self.MainWindow, "Success", "Transaction saved successfully!")

    def link_transaction_to_user(self, transaction_no):
        dc = DataConnector()
        mtuser_transactions = dc.get_all_mtuser_transactions()
        category_detail = None
        if self.radioButtonFoodDrink.isChecked():
            category_detail = "FoodDrink"
        elif self.radioButtonMoving.isChecked():
            category_detail = "Moving"
        elif self.radioButtonShopping.isChecked():
            category_detail = "Shopping"
        elif self.radioButtonInvoice.isChecked():
            category_detail = "Invoice"
        elif self.radioButtonOthers.isChecked():
            category_detail = "Others"
        new_link = MTuser_Transaction(self.main_ui.user_name, transaction_no, category_detail)
        mtuser_transactions.append(new_link)
        dc.update_mtuser_transactions(mtuser_transactions)