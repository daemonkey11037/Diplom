import csv
import re

def vuln_check():
    x = 'x'
    y = 'y'
    with open('vullist.csv', encoding='utf8') as vullist:
        reader = csv.reader(vullist)
        for row in reader:
            print('-----')
            for i in range(len(str(row[5]).split(" "))):
                if str(row[5]).split(" ")[i] == 'от':
                    print(str(row[5]).split(" ")[i+1])
                    x = str(row[5]).split(" ")[i+1]
                if str(row[5]).split(" ")[i] == 'до':
                    print(str(row[5]).split(" ")[i+1])
                    y = str(row[5]).split(" ")[i+1]
            print(x + ' - ' + y)
            print('-----')

def vuln_check2():
    with open('vullist.csv', encoding='utf8') as vullist:
        reader = csv.DictReader(vullist)
        for row in reader:
            print(row)

vuln_check2()#

