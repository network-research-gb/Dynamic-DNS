from flask import Flask

import dns.update
import dns.query
import dns.tsigkeyring
import dns.resolver

app = Flask(__name__)

@app.route('/query/<t>/<fqdn>')
def query(t, fqdn):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['127.0.0.1']
    answer = dns.resolver.query(fqdn, t)
    if t == 'a':
        return '{0}\n'.format(answer.rrset[0].address)

@app.route("/update/<domain>/<host>/<ip>", methods=['POST'])
def update(domain, host, ip):

    keyring = dns.tsigkeyring.from_text({
        'rndc-key' : 'myRNDCkey=='
    })

    update = dns.update.Update('{0}.'.format(domain), keyring=keyring)
    update.replace(host, 300, 'A', ip)
    response = dns.query.tcp(update, '127.0.0.1', timeout=10)

    return "update with {0}\n".format(ip)

if __name__ == "__main__":
    app.run()
