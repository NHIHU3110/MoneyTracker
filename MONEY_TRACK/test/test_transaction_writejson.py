from MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MONEY_TRACK.models.Transaction import Transaction

transactions=[]
transactions.append(Transaction('T1','02/28/2025','500000','Money In', 'Salary'))
transactions.append(Transaction('T2','02/28/2025','50000','Money Out','Others'))
transactions.append(Transaction('T3','02/28/2025','10000','Money Out','Others'))
transactions.append(Transaction('T4','02/28/2025','20000','Money Out','Others'))
transactions.append(Transaction('T5','02/28/2025','100000','Money In','Allowance'))
transactions.append(Transaction('T6','02/28/2025','200000','Money Out','Others'))
transactions.append(Transaction('T7','02/28/2025','15000','Money In','Others'))
transactions.append(Transaction('T8','02/28/2025','25000','Money Out','Others'))
transactions.append(Transaction('T9','02/28/2025','50000','Money Out','Others'))
transactions.append(Transaction('T10','02/28/2025','40000','Money Out','Allowance'))
print('List of transactions: ')
for tr in transactions:
    print(tr)
jff=JsonFileFactory()
filename='../dataset/transactions.json'
jff.write_data(transactions,filename)