import sqlite3
from modules.functions import addr_range
from modules.scanner import Host, Ports

connection = sqlite3.connect('source/db.db', check_same_thread=False)
cursor = connection.cursor()

hosts = []

# def main(ip):

#     with open(f'logs/{ip}', 'r') as file:
#         first = file.read().split(" ")[1]

#     with open(f'logs/{ip}', 'r') as file:
#         second = file.read().split(" ")[6]

#     if first != second:
#         print('AAAAAAAAA')
#     else:
#         print('Ok')

def catch():

    cursor.execute("""SELECT * from Hosts""")
    hosts_from_db = cursor.fetchall()

    for host in hosts_from_db:
        ports = []
        cursor.execute(f"""SELECT * from Ports WHERE id_hosts = '{host[0]}'""")
        ports_from_db = cursor.fetchall()

        for port in ports_from_db:
            ports.append(Ports(port[2], port[3], port[4]))

        hosts.append(Host(host[1], host[2], host[3], host[4], ports, host[5], host[6]))

def output(input):

    
    output_list = []

    if input == 'all':
        
        for host in hosts:
            print('----------')
            print(f'host: {host.host} ({host.hostname})\nhoststate: {host.hoststate}    protocol: {host.proto}\n')
            for port in host.ports:
                print(f'port: {port.port}  |  service: {port.product}  |  version: {port.version}')
            print('----------')

    else:

        input = input.split(' ')
        
        for host in input:
            if '-' in host:
                to_list = addr_range(host)
                for i in to_list:
                    output_list.append(i)
            else:
                output_list.append(host)

        for host in hosts:
            if host.host in output_list:
                print('----------')
                print(f'host: {host.host} ({host.hostname})\nhoststate: {host.hoststate}    protocol: {host.proto}\n')
                for port in host.ports:
                    print(f'port: {port.port}  |  service: {port.product}  |  version: {port.version}')
                print('----------')

def main(input):
    catch()
    output(input)
