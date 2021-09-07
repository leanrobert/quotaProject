import re

def check_client_in_file(file_name, clientIp):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if clientIp in line:
                match = re.findall("\d*]", line)
                return match[0][:-1]

print(check_client_in_file("counters.txt", "192.168.27.100"))