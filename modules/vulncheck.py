import sqlite3
import csv

connection = sqlite3.connect('/opt/archael/source/db.db', check_same_thread=False)
cursor = connection.cursor()

def vuln_search():
    vuln = []
    cursor.execute("""SELECT product, version, id_hosts FROM Ports""")
    list = cursor.fetchall()
    with open ('source/vullist.csv', encoding='utf8') as vullist:
        reader = csv.reader(vullist)
        for service in list:
            if service[0] == '' and service[1] == '':
                continue
            else:
                for row in reader:
                    if service[0].lower() == row[4].lower():
                        vuln.append(row[0])

    print(vuln)
    return vuln

def vuln_check(vuln):
    x = 0
    y = 0
    with open('source/vullist.csv', encoding='utf8') as vullist:
        reader = csv.reader(vullist)
        vulnerables = []
        for row in reader:
            if row[0] in vuln:
                for i in range(len(str(row[5]).split(" "))):
                    if str(row[5]).split(" ")[i] == 'от':
                        x = str(row[5]).split(" ")[i+1]
                    if str(row[5]).split(" ")[i] == 'до':
                        y = str(row[5]).split(" ")[i+1]
                    cursor.execute("""SELECT version FROM Ports WHERE product = '%s'""" % row[4].lower())
                    version = cursor.fetchall()[0][0]
                    if version > x and float(version) < float(y):
                        if f'{row[0]}: {row[4]}: ({version}) {x} - {y}' in vulnerables:
                            continue
                        else:
                            vulnerables.append(f'''
                            Идентификатор уязвимости: {row[0]}
                            Уязвимое ПО: {row[4]} ({version})
                            Уязвимые версии: {x} - {y}\n{row[12]}
                            --------------------''')
        for i in vulnerables:
            print(i)

def main():
    vuln_check(vuln_search())