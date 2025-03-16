from MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MONEY_TRACK.models.MTuser_Transaction import MTuser_Transaction

jff=JsonFileFactory()
filename='../dataset/mtuser_transactions.json'
mtuts=jff.read_data(filename,MTuser_Transaction)
print('List transactions of each MTusers: ')
for mtut in mtuts:
    print(mtut)
