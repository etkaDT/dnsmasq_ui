from flask import Flask, render_template
import sys
import time
app = Flask(__name__)

leases_file = ""

@app.route('/', methods=['GET'])
def main():
    leases = []
    with open(leases_file, "r") as f:
        for line in f:
            fields = line.split()
            ts = time.strftime("%d/%m/%Y - %H:%M:%S", time.localtime(int(fields[0])))
            leases.append({"ts": ts, "mac": fields[1], "ip": fields[2], "hostname": fields[3]})

    return render_template("dnsmasq.html", leases = leases)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No lease file specified!")
        exit(1)
    else:
        leases_file = sys.argv[1]

    app.run(host='0.0.0.0', debug = False)
