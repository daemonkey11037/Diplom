import socket
import os
import os.path
import subprocess
import time
import datetime

def service_file_creation():
    path = ''

    for i in subprocess.check_output('pwd', shell=True, text=True).rstrip():
        path = path + i
        if i == '\n':
            break
    path_with_macscan = path = '/macscan.py'

    service_create = """
    [Unit]
    Description=macscan
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python3.7 -u %s --wait
    Type=idle
    KillMode=process

    SyslogIdentifier=smart-test
    SyslogFacility=daemon

    [Install]
    WantedBy=multi-user.target\n""" % path_with_macscan

    with open ("/lib/systemd/system/macscan.service", "w") as service:
        service.write(service_create)

    os.system("systemctl daemon-reload")
    os.system("systemctl start macscan.service")
    os.system("systemctl enable macscan.service")

    if subprocess.check_output("systemctl status macscan.service | grep 'running'", shell=True, text=True) != '':
        print('Сервис успешно создан!')
    else:
        print('Что-то пошло не так!')
    exit()

def main():

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    udp_host = '192.168.0.2'
    udp_port = 12345
    path_to_save = "/macscan/storage/"

    sock.bind((udp_host, udp_port))

    while True:
        print("Waiting for client...")
        data,addr = sock.recvfrom(1024)
        print("Recevied Messages: ", data.strip().decode("utf-8"), addr[0])
        text = addr[0]

        dt = datetime.datetime.now()
        ct = dt.strftime('%H:%M:%S')
        cd = dt.strftime('%d-%m%Y')

        data = data.strip()
        array_data = data.split()
        array_data_decoded = array_data[0].decode('utf-8')
        fname = path_to_save + str(array_data_decoded)

        text = f"""
[*] {text}  {str(array_data_decoded)}   >>{cd} | {ct}<<
"""
        
        try:
            subprocess.check_output("ls /macscan/storage | grep '%s'" % str(array_data_decoded), shell=True, text=True)
            try:
                try:
                    print(fname)
                    print(str(array_data_decoded))
                    subprocess.check_output(f"cat {fname} | grep {addr[0]}", shell=True, text=True)
                except:
                    with open(fname, "r+") as file:
                        content = file.read()
                        file.seek(0, 0)
                        file.write(text)
                        file.write(content)
            except:
                pass
        except:
            try:
                with open(fname, "w") as file:
                    file.write(text)
            except:
                pass

while True:
    try:
        service_file_check = subprocess.check_output("ls /lib/systemd/system | grep 'macscan.service'", shell=True, text=True)
        try:
            subprocess.check_output("ls / | grep 'macscan'", shell=True, text=True)
        except:
            os.system("mkdir /macscan && mkdir /macscan/storage")
        try:
            subprocess.check_output("systemctl status macscan | grep 'running'", shell=True, text=True)
            main()
        except:
            os.system("systemctl restart macscan")
            time.sleep(1)
            exit()
    
    except:
        service_file_creation()

