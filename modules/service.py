import os

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
