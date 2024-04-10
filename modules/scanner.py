import nmap
import socket
import time
import threading
import sqlite3
import csv

connection = sqlite3.connect('source/db.db', check_same_thread=False)
cursor = connection.cursor()

reg = '^\d+\.\d+\.\d+\.\d+&'

# !-----Функция, которая сканирует хосты в сети и их порты-----!
def portscan(ip, port):
    nm = nmap.PortScanner()
    nm.scan(ip, port)

    # !-----Определение хостов-----!
    for host in nm.all_hosts():      
        cursor.execute("""SELECT host FROM Hosts""")
        list = cursor.fetchall()
        if len(list) == 0:
            try:
                cursor.execute("""INSERT INTO Hosts (host, hostname, host_state) VALUES ('%s', '%s', '%s');""" % (host, socket.gethostbyaddr(host)[0], nm[host].state()))
                connection.commit()
            except socket.herror:
                cursor.execute("""INSERT INTO Hosts (host, hostname, host_state) VALUES ('%s', '%s', '%s');""" % (host, '', nm[host].state()))
                connection.commit()
        else:
            skip = 0
            for address in list:
                if str(host) == str(address[0]):
                    skip = 1
            if skip == 0:
                try:
                    cursor.execute("""INSERT INTO Hosts (host, hostname, host_state) VALUES ('%s', '%s', '%s');""" % (host, socket.gethostbyaddr(host)[0], nm[host].state()))
                    connection.commit()
                except socket.herror:
                    cursor.execute("""INSERT INTO Hosts (host, hostname, host_state) VALUES ('%s', '%s', '%s');""" % (host, '', nm[host].state()))
                    connection.commit()

        # !-----Определение протокола передачи-----!
        for proto in nm[host].all_protocols():
            cursor.execute("""UPDATE Hosts SET protocol = '%s' WHERE host = '%s'""" % (proto, host))
            connection.commit

            lport = nm[host][proto].keys()
                    
            # !-----Определение открытых портов хоста-----!    
            for port in lport:
                cursor.execute("""SELECT id_hosts, port FROM Ports""")
                list = cursor.fetchall()
                cursor.execute("""SELECT id FROM Hosts WHERE host = '%s'""" % host)
                id = cursor.fetchall()[0][0]
                if len(list) == 0:
                    cursor.execute("""INSERT INTO Ports (id_hosts, port, product, version) VALUES ('%s', '%s', '%s', '%s')""" % (id, port, nm[host][proto][port]['product'], nm[host][proto][port]['version']))
                    connection.commit()
                else:
                    stopit = 0
                    for i in range(0, len(list)):
                        if int(id) == int(list[i][0]) and int(port) == int(list[i][1]):
                            stopit = 1
                    if stopit == 0:
                        cursor.execute("""INSERT INTO Ports (id_hosts, port, product, version) VALUES ('%s', '%s', '%s', '%s')""" % (id, port, nm[host][proto][port]['product'], nm[host][proto][port]['version']))
                        connection.commit()
                list.clear()

# !-----Вывод результата в консоль-----!
def output():
    cursor.execute("""SELECT count(*) FROM Hosts""")
    for host in range(1, cursor.fetchall()[0][0]+1):
        print('-------------------------------------')
        cursor.execute("""SELECT host, hostname, host_state, protocol FROM Hosts WHERE id = '%s'""" % host)
        list = cursor.fetchall()
        print('Host: %s (%s) is %s\tProtocol: %s' % (list[0][0], list[0][1], list[0][2], list[0][3]))
        list.clear()
        cursor.execute("""SELECT port, product, version FROM Ports WHERE id_hosts = '%s'""" % host)
        list = cursor.fetchall()
        for port in range(1, len(list)+1):
            print('Port: %s\tProduct: %s (%s)' % (list[port-1][0], list[port-1][1], list[port-1][2]))
        list.clear()
        print('-------------------------------------')

def clean(mode):
    mode = 'Y'
    if mode == 'Y':
        cursor.execute("""DROP TABLE Ports""")
        connection.commit()
        cursor.execute("""DROP TABLE Hosts""")
        connection.commit()

        cursor.executescript('''CREATE TABLE IF NOT EXISTS Hosts (
                        id INTEGER PRIMARY KEY,
                        host TEXT NOT NULL,
                        hostname TEXT,
                        host_state TEXT,
                        protocol TEXT
        );
                        PRAGMA foreign_key=on;
                        CREATE TABLE IF NOT EXISTS Ports (
                        id INTEGER PRIMARY KEY,
                        id_hosts INTEGER,
                        port TEXT NOT NULL,
                        product TEXT,
                        version TEXT,
                        FOREIGN KEY (id_hosts) REFERENCES Hosts (id)
        );''')
        connection.commit()

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
                            vulnerables.append(f'Идентификатор уязвимости: {row[0]}\nУязвимое ПО: {row[4]} ({version})\nУязвимые версии: {x} - {y}\n{row[12]}\n--------------------')
        for i in vulnerables:
            print(i)
                        

def main(ip):

        #clean()

        #ip = input("Введите диапозон ip-адресов: ")
        
        start_time = time.time()
        t1 = threading.Thread(target=portscan, args=(ip, '1-340'), daemon=True)
        t2 = threading.Thread(target=portscan, args=(ip, '341-683'), daemon=True)
        t3 = threading.Thread(target=portscan, args=(ip, '684-1024'), daemon=True)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()

        output()
        print("--- %s seconds ---\n" % (time.time() - start_time))
        print('Результат сохранён! Используйте аргумент -o для просмотра текущего списка адресов!')

        
# !-----Main-----!
if __name__ == '__main__':
    main()