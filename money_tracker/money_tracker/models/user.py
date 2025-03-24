class MTuser:
    """
    User model representing a Money Tracker user.
    """
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        
    def to_dict(self):
        """Convert the user object to a dictionary for JSON serialization"""
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a user object from a dictionary"""
        return cls(data["name"], data["username"], data["password"])