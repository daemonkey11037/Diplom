import nmap
import time
import socket
import sqlite3

reg = '^\d+\.\d+\.\d+\.\d+&'

connection = sqlite3.connect('source/db.db', check_same_thread=False)
cursor = connection.cursor()

class Ports:
    def __init__(self, port, product, version):
        self.port = port
        self.product = product
        self.version = version

class Host:
    def __init__(self, host, hostname, hoststate, proto, ports):
        self.host = host
        self.hostname = hostname
        self.hoststate = hoststate
        self.proto = proto
        self.ports = ports

hosts = []

def db_create():

    cursor.executescript('''CREATE TABLE IF NOT EXISTS Hosts (
                        id INTEGER PRIMARY KEY,
                        host TEXT NOT NULL,
                        hostname TEXT,
                        host_state TEXT,
                        protocol TEXT,
                        date TEXT,
                        time TEXT
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

def portscan(ip, port):
    nm = nmap.PortScanner()
    nm.scan(ip, port, '-T4 --min-parallelism 10 -A')

    for host in nm.all_hosts():
        print(host)

    for host in nm.all_hosts():

        ports = []
        
        for proto in nm[host].all_protocols():

            lport = nm[host][proto].keys()
                       
            for port in lport:
                ports.append(Ports(port=port, product=nm[host][proto][port]['name'], version=nm[host][proto][port]['version']))

        hosts.append(Host(host=host, hostname=hostname_check(host), hoststate=nm[host].state(), proto=0, ports=ports))

def db_add():
    for host in hosts:
        cursor.execute(f"""SELECT id from Hosts WHERE host = '{host.host}'""")
        en = cursor.fetchall()

        if en == []:

            cursor.execute(f"""INSERT INTO Hosts (host, hostname, host_state, protocol, date, time) VALUES ('{host.host}',
            '{host.hostname}', '{host.hoststate}', '{host.proto}', '{str(time.strftime("%d.%m.%Y"))}',
            '{str(time.strftime("%H:%M:%S"))}')""")
            connection.commit()

            cursor.execute(f"""SELECT id from Hosts WHERE host = '{host.host}'""")
            id = cursor.fetchall()[0][0]
            for port in host.ports:
                cursor.execute(f"""INSERT INTO Ports (id_hosts, port, product, version) VALUES ('{id}', '{port.port}',
                '{port.product}', '{port.version}')""")
                connection.commit()

        else:

            cursor.execute(f"""UPDATE Hosts SET hostname = '{host.hostname}', host_state = '{host.hoststate}',
            date = '{str(time.strftime("%d.%m.%Y"))}', time = '{str(time.strftime("%H:%M:%S"))}' WHERE host = '{host.host}'""")
            connection.commit()

            cursor.execute(f"""SELECT id from Hosts WHERE host = '{host.host}'""")
            id = cursor.fetchall()[0][0]
            for port in host.ports:
                cursor.execute(f"""SELECT port FROM Ports WHERE id_hosts = '{en[0][0]}'""")
                ports = cursor.fetchall()
                for port2 in ports:
                    if str(port.port) == str(port2[0]):
                        cursor.execute(f"""UPDATE Ports SET product = '{port.product}',
                        version = '{port.version}' WHERE port = '{port.port}'""")
                        connection.commit()
                        available = True

                if available == False:
                    cursor.execute(f"""INSERT INTO Ports (id_hosts, port, product, version) VALUES ('{id}',
                    '{port.port}', '{port.product}', '{port.version}')""")
                    connection.commit()
                available = False
                    
def hostname_check(host):
    try:
        result = socket.gethostbyaddr(host)[0]
    except:
        result = 'unknown'
    return result

def output():
    for host in hosts:
        print('----------')
        print(f'host: {host.host} ({host.hostname})\nhoststate: {host.hoststate}    protocol: {host.proto}\n')
        for port in host.ports:
            print(f'port: {port.port}  |  service: {port.product}  |  version: {port.version}')
        print('----------')

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
                        protocol TEXT,
                        date TEXT,
                        time TEXT
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

def datetime():
    current_date = time.strftime("%d.%m.%Y")
    current_time = time.strftime("%H:%M")                     

def main(ip):

        start_time = time.time()
       
        db_create()
        portscan(ip, '1-1024, 1434, 1723, 1900, 3306, 3389, 4500, 5900, 8080, 49152')
        output()
        db_add()
        hosts.clear()
        print("--- %s seconds ---\n" % (time.time() - start_time))

        

if __name__ == '__main__':
    main()