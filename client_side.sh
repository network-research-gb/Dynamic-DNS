#!/bin/sh

PATH=${PATH}:/sbin:/usr/sbin:/bin:/usr/bin:/usr/pkg/bin

name="mybox"
domain="mydomain"
# Fully qualified domain name
fqdn="${name}.${domain}"
# access into Ubuntu server 
auth="user:password"

# retrieve your actual public IP from a website like httpbin.org
curip=$(curl -s -o- http://httpbin.org/ip)
# fetch recorded IP address
homeip=$(curl -u ${auth} -s -o- https://your.public.server/dyndns/query/a/${fqdn})

if [ "${curip}" != "${homeip}" ]; then
        warnmsg="/!\\ home IP changed to ${curip} /!\\"

        echo "${warnmsg}"|mail -s "${warnmsg}" me@mydomain.net
        # Update address to httpbin.org/ip
        curl -u ${auth} \
                -X POST https://my.public.server/dyndns/update/${domain}/${name}/${curip}
fi
