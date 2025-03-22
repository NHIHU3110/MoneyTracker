from MoneyTracker.MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MoneyTracker.MONEY_TRACK.models.MTuser import MTuser

jff=JsonFileFactory()
filename= '../dataset/mtusers.json'
mtusers=jff.read_data(filename, MTuser)
print('List of MTusers after reading file: ')
for u in mtusers:
    print(u)
