import json
import os
import os.path

from money_tracker.models import MTuser, Transaction, MTuser_Transaction

# Path to the data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')
USER_TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'user_transactions.json')

def save_users(users):
    """
    Save users to JSON file
    
    Args:
        users (list): List of MTuser objects
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(USERS_FILE, "w") as f:
            json.dump([user.to_dict() for user in users], f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False
        
def load_users():
    """
    Load users from JSON file
    
    Returns:
        list: List of MTuser objects
    """
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                return [MTuser.from_dict(user_data) for user_data in data]
        else:
            # Create empty users file
            with open(USERS_FILE, "w") as f:
                json.dump([], f)
    except Exception as e:
        print(f"Error loading users: {e}")
    return []

def save_transactions(transactions):
    """
    Save transactions to JSON file
    
    Args:
        transactions (list): List of Transaction objects
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(TRANSACTIONS_FILE, "w") as f:
            json.dump([trans.to_dict() for trans in transactions], f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving transactions: {e}")
        return False
        
def load_transactions():
    """
    Load transactions from JSON file
    
    Returns:
        list: List of Transaction objects
    """
    try:
        if os.path.exists(TRANSACTIONS_FILE):
            with open(TRANSACTIONS_FILE, "r") as f:
                data = json.load(f)
                return [Transaction.from_dict(trans_data) for trans_data in data]
        else:
            # Create empty transactions file
            with open(TRANSACTIONS_FILE, "w") as f:
                json.dump([], f)
    except Exception as e:
        print(f"Error loading transactions: {e}")
    return []

def save_user_transactions(user_transactions):
    """
    Save user transactions to JSON file
    
    Args:           
        user_transactions (list): List of MTuser_Transaction objects
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(USER_TRANSACTIONS_FILE, "w") as f:
            json.dump([ut.to_dict() for ut in user_transactions], f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user transactions: {e}")
        return False
        
def load_user_transactions():
    """
    Load user transactions from JSON file
    
    Returns:
        list: List of MTuser_Transaction objects
    """
    try:
        if os.path.exists(USER_TRANSACTIONS_FILE):
            with open(USER_TRANSACTIONS_FILE, "r") as f:
                data = json.load(f)
                return [MTuser_Transaction.from_dict(ut_data) for ut_data in data]
        else:
            # Create empty user_transactions file
            with open(USER_TRANSACTIONS_FILE, "w") as f:
                json.dump([], f)
    except Exception as e:
        print(f"Error loading user transactions: {e}")
    return []

def save_savings_goals(username, goals):
    """
    Save user's savings goals to JSON file
    
    Args:
        username (str): Username
        goals (list): List of savings goal dictionaries
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        savings_file = os.path.join(DATA_DIR, f"{username}_savings.json")
        with open(savings_file, "w") as f:
            json.dump(goals, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving savings goals: {e}")
        return False
        
def load_savings_goals(username):
    """
    Load user's savings goals from JSON file
    
    Args:
        username (str): Username
        
    Returns:
        list: List of savings goal dictionaries
    """
    try:
        savings_file = os.path.join(DATA_DIR, f"{username}_savings.json")
        if os.path.exists(savings_file):
            with open(savings_file, "r") as f:
                return json.load(f)
        else:
            # Create empty savings file
            with open(savings_file, "w") as f:
                json.dump([], f)
    except Exception as e:
        print(f"Error loading savings goals: {e}")
    return []