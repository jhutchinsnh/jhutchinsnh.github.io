"""
whoami
===

This script launches a pseudo-DNS resolver which responds to
all queries for the chosen hostname with the requester's own
IP address. This will allow a client to definitively identify
their recursive resolver for use with geolocational lookups.

Requirements:

    Python 2.7+
    dnslib 0.9.4+ (pip install dnslib)
    ipaddress 1.0.14+ (pip install ipaddress)
    requests 2.20.1+ (pip install requests) (optional)

Sample usage:

    sudo python whoami.py
        --host local.test
        --port 9999
        --logfile /var/log/whoami.log

Parameters:

    --host [FQDN | "any"]
        Only return responses for valid hostnames, or to all hostnames (less secure)

    --port
        DNS response port (default 53, may be privileged and require sudo)

    --logfile
        Destination log file (leave blank for stdout)

Version 1.3
"""

from dnslib.server import DNSServer, BaseResolver, DNSLogger
from dnslib import RR, QTYPE, A, TXT, AAAA, RCODE, NS, SOA
from time import sleep, strftime
import signal
import os
import argparse
import sys
import ipaddress

# Get our external IP via checkip.dyn.com, for NS records
try:
    import requests
    checkip = requests.get('http://checkip.dyn.com')
    myip = str(re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', checkip.text).group())
# If requests isn't installed or something prevents checkip from responding correctly, just use a bogus IP
except:
    myip = "1.2.3.4"


# Handler for SIGTERM if daemonized via systemd
def dhandler(signum, frame):
    print("{} Received SIGTERM, exited successfully.".format(strftime("%Y-%m-%d %H:%M:%S")))
    exit()


# Overrides certain default behaviors of DNSLogger, namely formatting
class WhoAmILogger(DNSLogger):

    # YYYY-MM-DD HH:MM:SS Inbound:  [IP:PORT] (UDP/TCP) FQDN: 'fqdn.' Record Type: (TYPE)
    # 2020-09-20 16:41:01 Inbound:  [127.0.0.1:44673] (udp) FQDN: 'local.test.' Record Type: (ANY)
    def log_request(self, handler, request):
        print("{} Inbound:  [{}:{}] ({}) FQDN: '{}' Record Type:  {}".format(
            strftime("%Y-%m-%d %H:%M:%S"),
            handler.client_address[0],
            handler.client_address[1],
            handler.protocol,
            request.q.qname,
            QTYPE[request.q.qtype]))
        sys.stdout.flush()
        self.log_data(request)

    # YYYY-MM-DD HH:MM:SS Outbound: [IP:PORT] (UDP/TCP) FQDN: 'fqdn.' Response RRs: (TYPE(S))
    # 2020-09-20 16:41:55 Outbound: [127.0.0.1:58873] (udp) FQDN: 'local.test.' Response RRs: A,TXT,NS,NS,SOA
    def log_reply(self,handler,reply):
        print("{} Outbound: [{}:{}] ({}) FQDN: '{}' Response RRs: {}".format(
            strftime("%Y-%m-%d %H:%M:%S"),
            handler.client_address[0],
            handler.client_address[1],
            handler.protocol,
            reply.q.qname,
            ",".join([QTYPE[a.rtype] for a in reply.rr])))
        sys.stdout.flush()
        self.log_data(reply)


# Overrides default behaviors for BaseResolver, since this isn't a full nameserver
class WhoAmIResolver(BaseResolver):

    def __init__(self, zone, host):
        self.rrs = RR.fromZone(zone)
        self.host = host

    def resolve(self, request, handler):
        reply = request.reply()

        # IP of inbound DNS request
        yourip = ipaddress.ip_address(unicode(handler.client_address[0]))

        # Wildcards if the --host supplied is 'any', otherwise limits to predefined --host
        if str(self.host).lower() == "any":
            hostname = str(request.q.qname)
        else:
            hostname = self.host

        # Build standard record contents for reply
        # e.g. local.test.	60	IN	SOA	ns1.local.test. hostmaster.local.test. 1 3600 600 604800 60
        soar = SOA("ns1." + hostname,
                   "hostmaster." + hostname,
                   (1, 3600, 600, 604800, 60))
        # e.g. local.test.	60	IN	NS	ns1.local.test.
        #      local.test.	60	IN	NS	ns2.local.test.
        ns1r = NS("ns1." + hostname)
        ns2r = NS("ns2." + hostname)

        """
        Request construction
          Verify that the request is valid, which records were requested, and construct the response
          Uses add_answer for Answer and add_auth for Authority response sections
        """

        # Matching hostname or --host 'any' was used
        if request.q.qname == hostname:

            # A record
            if QTYPE[request.q.qtype] == "A":
                # If A was requested but inbound is v6, return SOA with NOERROR ("no problem but nothing found")
                if type(yourip) == ipaddress.IPv6Address:
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.SOA,
                        rdata=soar,
                        ttl=60))
                    reply.header.rcode = RCODE.NOERROR
                # Otherwise return NS1, NS2, and A
                else:
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.NS,
                        rdata=ns1r,
                        ttl=60))
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.NS,
                        rdata=ns2r,
                        ttl=60))
                    reply.add_answer(RR(
                        hostname,
                        QTYPE.A,
                        rdata=A(str(yourip)),
                        ttl=60))

            # AAAA record
            elif QTYPE[request.q.qtype] == "AAAA":
                # If AAAA was requested but inbound is v4, return SOA with NOERROR ("no problem but nothing found")
                if type(yourip) == ipaddress.IPv4Address:
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.SOA,
                        rdata=soar,
                        ttl=60))
                    reply.header.rcode = RCODE.NOERROR
                # Otherwise return NS1, NS2, and AAAA
                else:
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.NS,
                        rdata=ns1r,
                        ttl=60))
                    reply.add_auth(RR(
                        hostname,
                        QTYPE.NS,
                        rdata=ns2r,
                        ttl=60))
                    reply.add_answer(RR(
                        hostname,
                        QTYPE.A,
                        rdata=AAAA(str(yourip)),
                        ttl=60))

            # TXT record
            #   Return NS1, NS2, and human-formatted TXT with IP address
            elif QTYPE[request.q.qtype] == "TXT":
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns1r,
                    ttl=60))   
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns2r,
                    ttl=60))
                reply.add_answer(RR(
                    hostname,
                    QTYPE.TXT,
                    rdata=TXT("Your IP is " + str(yourip)),
                    ttl=60))
            
            # NS record
            #   Return just NS1 and NS2
            elif QTYPE[request.q.qtype] == "NS":
                reply.add_answer(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns1r,
                    ttl=43200))
                reply.add_answer(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns2r,
                    ttl=43200))

            # SOA record
            #   Return just SOA
            elif QTYPE[request.q.qtype] == "SOA":
                reply.add_answer(RR(
                    hostname,
                    QTYPE.SOA,
                    rdata=soar,
                    ttl=60))

            # ANY record
            #   Returns A/AAAA, TXT, NS1, NS2, and SOA
            elif QTYPE[request.q.qtype] == "ANY":
                # AAAA for IPv6
                if type(yourip) == ipaddress.IPv6Address:
                    reply.add_answer(RR(
                        hostname,
                        QTYPE.A,
                        rdata=AAAA(str(yourip)),
                        ttl=60))
                # A for IPv4
                else:
                    reply.add_answer(RR(
                        hostname,
                        QTYPE.A,
                        rdata=A(str(yourip)),
                        ttl=60))
                # TXT
                reply.add_answer(RR(
                    hostname,
                    QTYPE.TXT,
                    rdata=TXT("Your IP is " + str(yourip)),
                    ttl=60))
                # NS1
                reply.add_answer(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns1r,
                    ttl=60))
                # NS2
                reply.add_answer(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns2r,
                    ttl=60))
                # SOA
                reply.add_answer(RR(
                    hostname,
                    QTYPE.SOA,
                    rdata=soar,
                    ttl=60))

            # All other types are invalid, e.g. MX or CNAME;
            #   Return only SOA and NOERROR ("no problem but nothing found")
            else:
                reply.add_auth(RR(
                    hostname,
                    QTYPE.SOA,
                    rdata=soar,
                    ttl=60))
                reply.header.rcode = RCODE.NOERROR

	# Respond with appropriate rset for NS1.hostname.tld (A/IPv4 only)
	#   Skipped for --host any, since we'd just use the same IP for NS1/NS2 anyway
        elif request.q.qname == "ns1." + hostname:
            # Only respond for A records, all others receive SOA and NOERROR ("no problem but nothing found")
            if QTYPE[request.q.qtype] == "A":
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns1r,
                    ttl=60))   
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns2r,
                    ttl=60))   
                reply.add_answer(RR(
                    "ns1." + hostname,
                    QTYPE.A,
                    rdata=A(myip),
                    ttl=60))
            else:
                reply.add_auth(RR(
                    hostname,
                    QTYPE.SOA,
                    rdata=soar,
                    ttl=60))   
                reply.header.rcode = RCODE.NOERROR

        # NS2.hostname.tld (A only)
        elif request.q.qname == "ns2." + hostname:
            # Only respond for A records, all others receive SOA and NOERROR ("no problem but nothing found")
            if QTYPE[request.q.qtype] == "A":
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns1r,
                    ttl=60))   
                reply.add_auth(RR(
                    hostname,
                    QTYPE.NS,
                    rdata=ns2r,
                    ttl=60))   
                reply.add_answer(RR(
                    "ns2." + hostname,
                    QTYPE.A,
                    rdata=A(myip),
                    ttl=60))
            else:
                reply.add_auth(RR(
                    hostname,
                    QTYPE.SOA,
                    rdata=soar,
                    ttl=60))
                reply.header.rcode = RCODE.NOERROR

        # Invalid host, correct domain? NXDOMAIN
        elif hostname in str(request.q.qname):
            reply.header.rcode = RCODE.NXDOMAIN
            reply.add_auth(RR(
                hostname,
                QTYPE.SOA,
                rdata=soar,   
                ttl=60))  
        
        # Invalid domain without --host any? REFUSED
        else:
            reply.header.rcode = RCODE.REFUSED

        # Return constructed rrset
        return reply


if __name__ == '__main__':

    # Set handler for systemd stop command
    signal.signal(signal.SIGTERM, dhandler)

    # Parameters
    #  -l, --logfile: target log file
    #  --host: target hostname, or 'any' for all hosts
    #  --port: target port
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--logfile",
        help="Writes queries to file (default: stdout)",
        default="")
    parser.add_argument("--host",
        help="Specifies a hostname for resolution, 'any' for wildcard (default: whoami.xxx.com)",
        default="local.test")
    parser.add_argument("--port",
        help="Binds a port for DNS requests (default: 53)",
        default=53)
    args = parser.parse_args()

    # Print informational message and swap stdout to logfile, if specified
    if args.logfile:
        try:
            print("{} Server listening for {} on port {}, please see {} for detail, CTRL+C to shut down".format(
                strftime("%Y-%m-%d %H:%M:%S"),
                args.host,
                args.port,
                args.logfile))
            sys.stdout = open(args.logfile, "a")
        except IOError:
            print("Can't open log file!")
            exit(1)

    # Build pseudo-resolver
    try:
        # Add the 'resolve' method to the new server with specified parameters
        resolver = WhoAmIResolver(". 60 IN A 255.255.255.255", args.host)
        # Add a logging mechanism for requests
        logger = WhoAmILogger(log="request,reply,truncated,error", prefix=False)
        # Construct the server object and attach the resolver and logger
        server = DNSServer(resolver=resolver, port=int(args.port), logger=logger)
    except Exception as e:
        # Needs sudo for 53
        if "Permission denied" in e:
            print("Permission denied: use sudo for privileged ports such as 53")
        else:
            print("Error: {}".format(e))
        exit()

    print("{} Server listening for {} on port {}, CTRL+C to shut down".format(
        strftime("%Y-%m-%d %H:%M:%S"),
        args.host,
        args.port))
    sys.stdout.flush()

    # Server will maintain open connection until interrupted by Ctrl-C or SIGTERM
    try:
        server.start()
        while server.isAlive():
            sleep(1)
    # Shut down on keyboard interrupt
    except KeyboardInterrupt:
        server.stop()
        print("{} Server exiting...".format(strftime("%Y-%m-%d %H:%M:%S")))
    except Exception as e:
        print("Error: {}".format(e))
        server.stop()
        exit()

    print("{} Exited successfully.".format(strftime("%Y-%m-%d %H:%M:%S")))
    sys.stdout.flush()
