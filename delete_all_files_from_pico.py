import os 

file_list = os.listdir()
print(file_list)

for item in file_list:
    os.remove(f'{item}')

file_list = os.listdir()

if file_list == []:
    print('ok')
else:
    print('Files were not deleted!!!')
