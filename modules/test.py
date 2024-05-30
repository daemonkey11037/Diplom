import subprocess

def main():

    output = subprocess.check_output('ls logs', shell=True, text=True)

    for file in output:

        with open(f'logs/{file}', 'r') as file:
            first = file.read().split(" ")[1]

        with open(f'logs/{file}', 'r') as file:
            second = file.read().split(" ")[6]

        if first != second:
            print(f'Несоответствие MAC-адреса для хоста {file}!')
        else:
            print('Несоответсвий не обнаружено')