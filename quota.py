import ipaddress
import random
import os

network = ipaddress.IPv4Network("192.168.5.0/24")
ips = []

for i in range(10):
    oct2 = random.choice(range(1, 254))
    #oct3 = random.choice(range(1, 254))
    #oct4 = random.choice(range(1, 254))
    ip = f'192.168.5.{oct2}'
    #ip = f'10.{oct2}.{oct3}.{oct4}'
    ips.append(ip)

ips.append('192.168.5.2')

markRules = []
jumpRules = []
clientRules = []
jumpGeneralRule = f'-A PREROUTING -j {network}\n'

markRules.append(f':{str(network)} - [0:0]\n')

def escribirReglas(ips, network):
    ipsSi = []

    for ip in ips:
        ip = ipaddress.IPv4Address(ip)
        if ip in network:
            ipsSi.append(ip)

    if len(ipsSi) > 4:
        networklist = list(network.subnets())
        
        netupper = networklist[0]
        markRules.append(f':{str(netupper)} - [0:0]\n')
        jumpRules.append(f'-A {str(network)} -s {str(netupper)} -j {str(netupper)}\n')

        netlower = networklist[1]
        markRules.append(f':{str(netlower)} - [0:0]\n')
        jumpRules.append(f'-A {str(network)} -s {str(netlower)} -j {str(netlower)}\n')

        escribirReglas(ipsSi, netlower)
        escribirReglas(ipsSi, netupper)
    else:
        if len(ipsSi) == 0:
            return
        else:
            for ip in ipsSi:
                clientRules.append(f'-A {str(network)} -s {str(ip)}/32 -j ACCEPT\n')
            return

escribirReglas(ips, network)
readfile = open("quota.txt", "r")
readed = readfile.readlines()
header = readed[0:7]
footer = readed[-2:]
readfile.close()

file = open("quota.txt", "w")
file.writelines(header)
file.writelines(markRules)
file.write(jumpGeneralRule)
file.writelines(jumpRules)
file.writelines(clientRules)
file.writelines(footer)





'''def reglaExiste(network, ip = '', jump = ''):
    if(jump == ''):
        if(ip == ''):
            result = os.system(f'/sbin/iptables -t mangle -C PREROUTING -j {network}')
        else:
            result = os.system(f'/sbin/iptables -t mangle -C {network} --src {ip}/32 -j ACCEPT')
    else:
        result = os.system(f'/sbin/iptables -t mangle -C {network} --src {ip} -j {jump}')

    return result


os.system(f'/sbin/iptables -t mangle -N {network}')

if reglaExiste(network) != 0:
    os.system(f'/sbin/iptables -t mangle -A PREROUTING -j {network}')

def subnetear(ips, network):
    ipsSi = []

    for ip in ips:
        ip = ipaddress.IPv4Address(ip)
        if ip in network:
            ipsSi.append(ip)

    if len(ipsSi) > 4:
        networklist = list(network.subnets())
        
        netupper = networklist[0]
        os.system(f'/sbin/iptables -t mangle -N {netupper}')
        if reglaExiste(network, str(netupper), str(netupper)) != 0:
            os.system(f'/sbin/iptables -t mangle -A {network} --src {str(netupper)} -j {str(netupper)}')
        
        netlower = networklist[1]
        os.system(f'/sbin/iptables -t mangle -N {netlower}')
        if reglaExiste(network, str(netlower), str(netlower)) != 0:
            os.system(f'/sbin/iptables -t mangle -A {network} --src {str(netlower)} -j {str(netlower)}')

        subnetear(ipsSi, netlower)
        subnetear(ipsSi, netupper)
    else:
        if len(ipsSi) == 0:
            return
        else:
            for ip in ipsSi:
                if reglaExiste(network, ip) != 0:
                    os.system(f'/sbin/iptables -t mangle -A {str(network)} --src {str(ip)}/32 -j ACCEPT')
            return

subnetear(ips, network)'''