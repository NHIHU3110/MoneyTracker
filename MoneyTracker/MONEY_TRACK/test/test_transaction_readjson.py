from MoneyTracker.MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MoneyTracker.MONEY_TRACK.models.Transaction import Transaction

jff=JsonFileFactory()
filename= '../dataset/transactions.json'
transactions=jff.read_data(filename, Transaction)
print('List of transactions after reading file: ')
for tr in transactions:
    print(tr)
    
