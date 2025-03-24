class MTuser_Transaction:
    """
    User Transaction model linking users to transactions.
    """
    def __init__(self, transaction_number, name):
        self.transaction_number = transaction_number  # ID của giao dịch
        self.name = name  # Tên người dùng
        
    def to_dict(self):
        """Convert the user transaction object to a dictionary for JSON serialization"""
        return {
            "transaction_number": self.transaction_number,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a user transaction object from a dictionary"""
        return cls(data["transaction_number"], data["name"])


