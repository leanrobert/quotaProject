import re, os, ipaddress, subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/quota/<clientIp>')
def get_quota_by_ip(clientIp):
    os.system("/sbin/iptables-save -t mangle -c -f counters.txt")
    clientIp32 = clientIp + "/32"
    with open("counters.txt", 'r') as read_obj:
        for line in read_obj:
            if clientIp32 in line:
                match = re.findall("\d*]", line)
                client = { "ip": clientIp, "qdownload": match[0][:-1]}
                return jsonify(client)

@app.route('/resetQuota')
def reset_quota():
    os.system('/sbin/iptables -t mangle -F')
    os.system('/sbin/iptables -t mangle -X')
    os.system('/sbin/iptables-save -t mangle -f quota.txt')
    os.system('/sbin/iptables-save -t mangle -f counters.txt')
    return(jsonify({ 'message': 'Ips reseteadas con exito'}))

@app.route('/generate', methods=['POST'])
def create_node_rules():
    def generarArchivos():
        readfile = open("quota.txt", "r")
        readed = readfile.readlines()
        header = readed[0:7]
        footer = readed[-2:]
        readfile.close()

        file = open("quota.txt", "w")
        file.writelines(header)
        file.writelines(markRules)
        file.writelines(jumpGeneralRule)
        file.writelines(jumpRules)
        file.writelines(clientRules)
        file.writelines(footer)

    def escribirReglas(ips, network):
        ipsSi = []

        for ip in ips:
            ip = ipaddress.IPv4Address(ip)
            if ip in network:
                ipsSi.append(ip)

        if len(ipsSi) > 4:
            networklist = list(network.subnets())
            
            netupper = networklist[0]
            markRules.append(":" + str(netupper) + " - [0:0]\n")
            jumpRules.append("-A {str(network)} -s {str(netupper)} -j {str(netupper)}\n")

            netlower = networklist[1]
            markRules.append(":" + str(netlower) + " - [0:0]\n")
            jumpRules.append("-A " + str(network) + " -s " + str(netlower) + " -j " + str(netlower) + "\n")

            escribirReglas(ipsSi, netlower)
            escribirReglas(ipsSi, netupper)
        else:
            if len(ipsSi) == 0:
                return
            else:
                for ip in ipsSi:
                    clientRules.append("-A " + str(network) + " -s " + str(ip) + "/32 -j ACCEPT\n")
                return

    markRules = []
    jumpRules = []
    clientRules = []
    jumpGeneralRule = []

    nodos = request.get_json()
    for subnet in nodos:
        network = ipaddress.IPv4Network("10." + str(subnet) + ".0.0/16")
        jumpGeneralRule.append("-A PREROUTING -j " + network + "\n")
        markRules.append(":" + str(network) + " - [0:0]\n")
        escribirReglas(nodos[subnet], network)   

    generarArchivos()
    return(jsonify({ 'message': 'reglas de mangle creadas con exito'}))

@app.route('/apply', methods=['POST'])
def apply_iptables_rules():
    cmd = ["/sbin/iptables-restore", "-T", "mangle", "quota.txt"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.communicate()
    return jsonify({ 'message': 'iptables executed'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    nodos = request.get_json()
    for subnet in nodos:
        print("la red es " + str(subnet) + " y tiene las ips " + str(nodos[subnet]))
    return("<h1>" + str(nodos) + "</h1>")



import re, os, ipaddress, subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/quota/<clientIp>')
def get_quota_by_ip(clientIp):
    os.system("/sbin/iptables-save -t mangle -c -f /var/www/quota/counters.txt")
    clientIp32 = clientIp + "/32"
    with open("/var/www/quota/counters.txt", 'r') as read_obj:
        for line in read_obj:
            if clientIp32 in line:
                match = re.findall("\d*]", line)
                client = { "ip": clientIp, "qdownload": match[0][:-1]}
                return jsonify(client)

@app.route('/resetQuota', methods=['POST'])
def reset_quota():
    os.system('sudo /sbin/iptables -t mangle -F')
    os.system('sudo /sbin/iptables -t mangle -X')
    os.system('sudo /sbin/iptables-save -t mangle -f /var/www/quota/quota.txt')
    os.system('sudo chmod 666 /var/www/quota/quota.txt')
    os.system('sudo /sbin/iptables-save -t mangle -f /var/www/quota/counters.txt')
    os.system('sudo chmod 666 /var/www/quota/counters.txt')
    return(jsonify({ 'message': 'Ips reseteadas con exito'}))

@app.route('/generate', methods=['POST'])
def create_node_rules():
    def generarArchivos():
        readfile = open("/var/www/quota/quota.txt", "r")
        readed = readfile.readlines()
        header = readed[0:7]
        footer = readed[-2:]
        readfile.close()

        file = open("/var/www/quota/quota.txt", "w")
        file.writelines(header)
        file.writelines(markRules)
        file.writelines(jumpGeneralRule)
        file.writelines(jumpRules)
        file.writelines(clientRules)
        file.writelines(footer)

    def escribirReglas(ips, network):
        ipsSi = []

        for ip in ips:
            ip = ipaddress.IPv4Address(ip)
            if ip in network:
                ipsSi.append(ip)

        if len(ipsSi) > 4:
            networklist = list(network.subnets())

            netupper = networklist[0]
            markRules.append(":" + str(netupper) + " - [0:0]\n")
            jumpRules.append("-A " + str(network) + " -s " + str(netupper) + " -j " + str(netupper) + "\n")
            netlower = networklist[1]
            markRules.append(":" + str(netlower) + " - [0:0]\n")
            jumpRules.append("-A " + str(network) + " -s " + str(netlower) + " -j " + str(netlower) + "\n")

            escribirReglas(ipsSi, netlower)
            escribirReglas(ipsSi, netupper)
        else:
            if len(ipsSi) == 0:
                return
            else:
                for ip in ipsSi:
                    clientRules.append("-A " + str(network) + " -s " + str(ip) + "/32 -j ACCEPT\n")
                return

    markRules = []
    jumpRules = []
    clientRules = []
    jumpGeneralRule = []

    nodos = request.get_json()
    for subnet in nodos:
        network = ipaddress.IPv4Network("10." + str(subnet) + ".0.0/16")
        jumpGeneralRule.append("-A PREROUTING -j " + str(network) + "\n")
        markRules.append(":" + str(network) + " - [0:0]\n")
        escribirReglas(nodos[subnet], network)

    generarArchivos()
    return(jsonify({ 'message': 'reglas de mangle creadas con exito'}))

@app.route('/apply', methods=['POST'])
def apply_iptables_rules():
    cmd = ["sudo", "/sbin/iptables-restore", "-T", "mangle", "/var/www/quota/quota.txt"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.communicate()
    return jsonify({ 'message': 'iptables executed'})

@app.route('/test', methods=['GET', 'POST'])
def test():
    nodos = request.get_json()
    for subnet in nodos:
        print("la red es " + str(subnet) + " y tiene las ips " + str(nodos[subnet]))
    return("<h1>" + str(nodos) + "</h1>")