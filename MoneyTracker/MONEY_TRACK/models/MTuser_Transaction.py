class MTuser_Transaction:
    def __init__(self, Name, TransactionID, Category):
        self.Name = Name
        self.TransactionID = TransactionID
        self.Category = Category
    def __str__(self):
        return f'{self.Name}\t{self.TransactionID}\t{self.Category}'
    def to_dict(self):
        return {"Name": self.Name, "TransactionID": self.TransactionID, "Category": self.Category}
