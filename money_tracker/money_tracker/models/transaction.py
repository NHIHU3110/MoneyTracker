# class Transaction:
#     """
#     Transaction model representing a money transaction.
#     """
#     def __init__(self, transaction_number, transaction_date, amount, category, category_detail):
#         self.transaction_number = transaction_number
#         self.transaction_date = transaction_date
#         self.amount = amount
#         self.category = category  # Money In/Money Out/Savings
#         self.category_detail = category_detail
        
#     def to_dict(self):
#         """Convert the transaction object to a dictionary for JSON serialization"""
#         return {
#             "transaction_number": self.transaction_number,
#             "transaction_date": self.transaction_date,
#             "amount": self.amount,
#             "category": self.category,
#             "category_detail": self.category_detail
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         """Create a transaction object from a dictionary"""
#         return cls(data["transaction_number"], data["transaction_date"], 
#                    data["amount"], data["category"], data["category_detail"])
import datetime
import uuid

class Transaction:
    """
    Transaction model representing a money transaction.
    """
    def __init__(self, transaction_number, transaction_date, amount, category, category_detail):
        self.transaction_number = transaction_number
        self.transaction_date = transaction_date
        self.amount = amount
        self.category = category  # Money In/Money Out/Savings
        self.category_detail = category_detail
        
    def to_dict(self):
        """Convert the transaction object to a dictionary for JSON serialization"""
        return {
            "transaction_number": self.transaction_number,
            "transaction_date": self.transaction_date,
            "amount": self.amount,
            "category": self.category,
            "category_detail": self.category_detail
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a transaction object from a dictionary"""
        return cls(data["transaction_number"], data["transaction_date"], 
                   data["amount"], data["category"], data["category_detail"])
    
    def get_formatted_date(self):
        """Return date in a formatted string"""
        if isinstance(self.transaction_date, str):
            return self.transaction_date
        elif isinstance(self.transaction_date, (datetime.date, datetime.datetime)):
            return self.transaction_date.strftime("%Y-%m-%d")
        return str(self.transaction_date)
    
    def get_formatted_amount(self):
        """Return amount in a formatted string with currency"""
        return f"{float(self.amount):,.0f} VND"


class UserTransaction:
    """
    Class representing a link between a user and a transaction
    """
    def __init__(self, name, transaction_number):
        self.name = name
        self.transaction_number = transaction_number