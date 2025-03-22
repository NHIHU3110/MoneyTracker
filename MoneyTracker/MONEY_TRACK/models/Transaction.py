# MONEY_TRACK/models/Transaction.py
class Transaction:
    def __init__(self, TransactionNo, TransactionDate, Amount, Category, CategoryDetail):
        self.TransactionNo = TransactionNo
        self.TransactionDate = TransactionDate
        self.Amount = Amount
        self.Category = Category
        self.CategoryDetail = CategoryDetail

    def __str__(self):
        return f'{self.TransactionNo}\t{self.TransactionDate}\t{self.Amount}\t{self.Category}\t{self.CategoryDetail}'

    def to_dict(self):
        return {
            "TransactionNo": self.TransactionNo,
            "TransactionDate": self.TransactionDate,
            "Amount": self.Amount,
            "Category": self.Category,
            "CategoryDetail": self.CategoryDetail
        }