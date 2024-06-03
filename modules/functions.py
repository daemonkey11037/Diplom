import os
import subprocess

def addr_range(input):

    list = []
    last_octet = input.split('.')[3]
    other_octets = f'''{input.split('.')[0]}.{input.split('.')[1]}.{input.split('.')[2]}.'''
    first_digit = int(last_octet.split("-")[0])
    second_digit = int(last_octet.split("-")[1])

    for addr in range(first_digit, second_digit+1):
        list.append(other_octets + str(addr))

    return list

def service_check():

    if 'archael_macscan.service' in subprocess.check_output('ls /etc/systemd/system', shell=True, text=True):
        return True
    
    else:
        cron_path = '/opt/archael/modules/cron.py'

        service_create = f"""
            [Unit]
            Description=macscan
            After=multi-user.target

            [Service]
            ExecStart=/usr/bin/python3.7 -u {cron_path} --wait
            Type=idle
            KillMode=process

            SyslogIdentifier=smart-test
            SyslogFacility=daemon

            [Install]
            WantedBy=multi-user.target\n"""

        with open('/etc/systemd/system/archael_macscan.service', 'w') as service_file:
            service_file.write(service_create)

        os.system('systemctl daemon-reload')
        os.system('systemctl start archael_macscan.service')
        os.system('systemctl enable archael_macscan.service')

        if subprocess.check_output("systemctl status macscan.service | grep 'running'", shell=True, text=True) != '':
            print('Сервис успешно создан!')
            return True
        else:
            print('Что-то пошло не так!')
            return False
