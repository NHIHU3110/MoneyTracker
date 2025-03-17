# python
from MoneyTracker.MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MoneyTracker.MONEY_TRACK.models.MTuser import MTuser
from MoneyTracker.MONEY_TRACK.models.MTuser_Transaction import MTuser_Transaction
from MoneyTracker.MONEY_TRACK.models.Transaction import Transaction
import logging


class DataConnector:
    def get_all_mtusers(self):
        jff = JsonFileFactory()
        filename = '../dataset/mtusers.json'
        return jff.read_data(filename, MTuser)

    def get_all_transactions(self):
        jff = JsonFileFactory()
        filename = '../dataset/transactions.json'
        transactions = jff.read_data(filename, Transaction)
        return transactions

    def get_all_mtuser_transactions(self):
        jff = JsonFileFactory()
        filename = '../dataset/mtuser_transactions.json'
        mtuts = jff.read_data(filename, MTuser_Transaction)
        return mtuts

    def login(self, username, password):
        mtusers = self.get_all_mtusers()
        for mtuser in mtusers:
            if mtuser.Username == username and mtuser.Password == password:
                return mtuser
        return None

    def update_transactions(self, transactions):
        jff = JsonFileFactory()
        filename = '../dataset/transactions.json'
        jff.write_data(transactions, filename)

    # python
    def update_mtuser_transactions(self, mtuser_transactions):
        jff = JsonFileFactory()
        filename = '../dataset/mtuser_transactions.json'
        jff.write_data(mtuser_transactions, filename)

    def get_transactions_by_name(self, name):
        user_transactions = self.get_all_mtuser_transactions()  # Sửa chỗ này

        if not user_transactions:
            logging.error(f"No transactions found for user '{name}'.")
            return []


        user_transactions = [tr for tr in user_transactions if tr.Name == name]
        transaction_ids = {tr.TransactionID for tr in user_transactions}

        all_transactions = self.get_all_transactions()
        filtered_transactions = [tr for tr in all_transactions if tr.TransactionNo in transaction_ids]

        return filtered_transactions




