from MONEY_TRACK.libs.JsonFileFactory import JsonFileFactory
from MONEY_TRACK.models.MTuser import MTuser

mtusers=[]
mtusers.append(MTuser('Tran Khanh Ly','lytran','123'))
mtusers.append(MTuser('Phan Thi Ngoc Khuyen','khuyenphan','123'))
mtusers.append(MTuser('Huynh Thao Nhi','nhihuynh','123'))
mtusers.append(MTuser('Tran Hac Huong Thu','thutran','123'))
mtusers.append(MTuser('Ho Ngoc Xuan Quyen','quyenho','123'))
print('List of MTusers: ')
for u in mtusers:
    print(u)
jff=JsonFileFactory()
filename='../dataset/mtusers.json'
jff.write_data(mtusers,filename)


mtusers_dict = [u.to_dict() for u in mtusers]
jff.write_data(mtusers_dict, filename)