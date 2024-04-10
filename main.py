import modules.scanner as scanner
import modules.passchecker as passchecker
import sqlite3
from colorama import Fore, Style
import argparse



#print('                    ______________        _____ ______ ____ ')
#rint('                   |   ________   |      / _   |   _  \ ___|')
#print('                   | _/  ____  \_ |     / /_|  |  |_\  \    ')
#print('                   ( >\ (O  O) /< )    /  __   | ______/___ ')
#print('                   ||_/\ \oo/ /\_||   /_/   |__|__| |______|')
#print('                   | / /\(==)/\ \ |                         ')
#print('                   |/ /###\/###\ \|                         ')
#print('                   |\ \########/ /|                         ')
#print('                   |______________|                         ')
#print('                                                            ')


#while True:
#    choise = input('ape(0.1) > ')
#
#    match choise:
#        case 'scan':
#            scanner.main()
#           print(' ')
#            input('Нажмите Enter...')
#        case 'vulnerables':
#            scanner.vuln_check(scanner.vuln_search())
#            input('Нажмите Enter...')
#        case 'passcheck':
#            password = input('Пароль: ')
#            passchecker.passcheck(password)
#            print(' ')
#            input('Нажмите Enter...')
#        case 'help':
#            print('''
#       -[ scan - сетевой сканер портов                                                   ]-
#       -[ vulnerables - проверить наличие уязвимостей (доступно после сканирования сети) ]-
#       -[ passcheck - проверка надёжности пароля                                         ]-
#                  ''')
#        case 'exit':
#            break
        
parser = argparse.ArgumentParser()
parser.add_argument('ip', nargs='?', default='0')
parser.add_argument('-w', '--without-output', action='store_true')
parser.add_argument('-c', '--clean', action='store_true')
parser.add_argument('-o', '--output', action='store_true')
parser.add_argument('-v', '--vulnerable-check', action='store_true')
args = parser.parse_args()

print(args)
if args.clean == True:
    scanner.clean(args.clean)
if args.ip != '0':
    print('Loading...')
    scanner.main(args.ip)
if args.output == True:
    scanner.output()
if args.vulnerable_check == True:
    scanner.vuln_check(scanner.vuln_search())