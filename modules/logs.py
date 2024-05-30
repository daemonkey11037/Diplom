def main(ip):

    with open(f'logs/{ip}', 'r') as file:
        first = file.read().split(" ")[1]

    with open(f'logs/{ip}', 'r') as file:
        second = file.read().split(" ")[6]

    if first != second:
        print('AAAAAAAAA')
    else:
        print('Ok')
