from MoneyTracker.MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MoneyTracker.MONEY_TRACK.models.MTuser_Transaction import MTuser_Transaction

mtuts=[]
mtuts.append(MTuser_Transaction('Tran Khanh Ly','T1','Money Out'))
mtuts.append(MTuser_Transaction('Phan Thi Ngoc Khuyen','T2','Money In'))
mtuts.append(MTuser_Transaction('Huynh Thao Nhi','T3','Money In'))
mtuts.append(MTuser_Transaction('Tran Khanh Ly','T2','Money Out'))
mtuts.append(MTuser_Transaction('Tran Khanh Ly','T3','Money Out'))
mtuts.append(MTuser_Transaction('Tran Khanh Ly','T4','Money Out'))
mtuts.append(MTuser_Transaction('Tran Khanh Ly','T5','Money Out'))
print('List transactions of each MTuser: ')
for mtut in mtuts:
    print(mtut)

jff=JsonFileFactory()
filename= '../dataset/mtuser_transactions.json'
jff.write_data(mtuts,filename)
