#!/usr/bin/env python
from netmiko import Netmiko
import os

path = "/home/jor/backup_mikrotik"
path_ips = path+"/ips.txt"
dir_backup = path+"/backups"

# cria diretorios caso nao exista
if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir(dir_backup)
    file_ips = open(path_ips, 'w')
    file_ips.write("#Digite seus ips de bakup a baixo, caso queria comentar adicione '#' na frente\n")
    file_ips.write("192.168.0.88")
    file_ips.close()


with open(path_ips) as ips:
   for cnt, ip in enumerate(ips):
       if ip[0] != "#":
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

             hostname = hostname.strip().replace('name: ', '').lower()

             #criando arquivo de backup
             filen= open(dir_backup+"/"+hostname+".rsc", 'w')
             filen.write(output)
             filen.close()

             print("Backup realizado com sucesso")
         except Exception as e:
             print("Ouve um erro :")
             print(e)
