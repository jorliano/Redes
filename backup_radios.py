#!/usr/bin/env python
from netmiko import Netmiko
import os

path = "/home/jor/backup_radio"
path_ips = path+"/ips.txt"
dir_backup = path+"/backups"

# cria diretorios caso nao exista
if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir(dir_backup)
    file_ips = open(path_ips, 'w')
    file_ips.write("192.168.1.20")
    file_ips.close()


with open(path_ips) as ips:
   for cnt, ip in enumerate(ips):
        print(ip)

        try:
            #dados da conexao do equipamento
            plataforma = {
                "host": ip,
                "username": "admin",
                "password": "admin",
                "device_type": "linux",
            }

            #conexao e comandos via ssh
            net_connect = Netmiko(**plataforma)
            print(net_connect.find_prompt())
            output = net_connect.send_command("cat /tmp/system.cfg")
            hostname = net_connect.send_command("cat /proc/sys/kernel/hostname")
            net_connect.disconnect()

            hostname = hostname.strip().lower()

            #criando arquivo de backup
            filen= open(dir_backup+"/"+hostname+".cfg", 'w')
            filen.write(output)
            filen.close()

            print("Backup realizado com sucesso")
        except Exception as e:
            print("Ouve um erro :")
            print(e)
