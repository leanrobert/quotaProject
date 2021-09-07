import re, os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/quota/<clientIp>')
def get_quota_by_ip(clientIp):
    os.system("sudo /sbin/iptables-save -t mangle -c -f counters.txt")
    clientIp32 = clientIp + "/32"
    with open("counters.txt", 'r') as read_obj:
        for line in read_obj:
            if clientIp32 in line:
                match = re.findall("\d*]", line)
                client = { "ip": clientIp, "qdownload": match[0][:-1]}
                return jsonify(client)