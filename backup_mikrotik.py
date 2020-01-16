#!/usr/bin/env python
from netmiko import Netmiko
import os

listaips = "/home/jor/Redes/listaips/ips.txt"
dir_backup = "/home/jor/Redes/backup"

with open(listaips) as ips:
   for cnt, ip in enumerate(ips):
        print(ip)

        try:
            #dados da conexao do equipamento
            plataforma = {
                "host": ip,
                "username": "admin",
                "password": "admin",
                "device_type": "mikrotik_routeros",
            }

            #conexao e comandos via ssh
            net_connect = Netmiko(**plataforma)
            print(net_connect.find_prompt())
            output = net_connect.send_command("export")
            hostname = net_connect.send_command("/system identity print")
            net_connect.disconnect()

            #definindo diretorio dos backups
            os.chdir(dir_backup)
            hostname = hostname.strip().replace('name: ', '').lower()

            #criando arquivo de backup
            filen= open(hostname+".rsc", 'w')
            filen.write(output)
            filen.close()

            print("Backup realizado com sucesso")
        except Exception as e:
            print("Ouve um erro :")
            print(e)
