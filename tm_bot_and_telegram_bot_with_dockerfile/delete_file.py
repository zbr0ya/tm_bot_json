import subprocess


def delete_file():
    delete = {'1': 'my_inventory_info.json', '2': 'skin_full_info.json'}
    user_input = input(f'{delete}:- delete -> ')
    if user_input == '1':
        subprocess.run(['rm', 'my_inventory_info.json'])
    elif user_input == '2':
        subprocess.run(['rm', 'skin_full_info.json'])
    else:
        print('command not found')


delete_file()