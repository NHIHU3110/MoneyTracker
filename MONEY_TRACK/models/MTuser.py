class MTuser:
    def __init__(self, Name, Username, Password):
        self.Name = Name
        self.Username = Username
        self.Password = Password
    def __str__(self):
        return f'{self.Name}\t{self.Username}\t{self.Password}'

    def to_dict(self):
        """Chuyển đối tượng thành dictionary để ghi vào JSON"""
        return {"Name": self.Name, "Username": self.Username, "Password": self.Password}