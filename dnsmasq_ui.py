from flask import Flask, render_template
import sys
import os
import time
app = Flask(__name__)

DEFAULT_LEASES_FILE = "/var/lib/misc/dnsmasq.leases"
leases_file = ""

@app.route('/', methods=['GET'])
def main():
    global leases_file
    leases = []
    with open(leases_file, "r") as f:
        for line in f:
            fields = line.split()
            ts = time.strftime("%d/%m/%Y - %H:%M:%S", time.localtime(int(fields[0])))
            leases.append({"ts": ts, "mac": fields[1], "ip": fields[2], "hostname": fields[3]})

    return render_template("dnsmasq.html", leases = leases)

@app.before_first_request
def get_leases_file():
    global leases_file
    if len(leases_file) != 0:
        # The file was defined using command line arguments.
        leases_file = sys.argv[1]
    elif 'DNSMASQ_LEASE_FILE' in os.environ:
        leases_file = os.environ['DNSMASQ_LEASE_FILE']
    elif os.path.isfile('/etc/dnsmasq_ui.conf'):
        with open('/etc/dnsmasq_ui.conf', 'r') as conf:
            leases_file = conf.read()
    elif os.path.isfile(DEFAULT_LEASES_FILE):
        leases_file = DEFAULT_LEASES_FILE
    else:
        print("No leases file specified!", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        leases_file = sys.argv[1]

    app.run(host='0.0.0.0', debug = False)
