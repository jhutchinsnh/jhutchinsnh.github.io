## README

[whoami.py](https://github.com/jhutchinsnh/jhutchinsnh.github.io/tree/master/whoami) requires Python 2.7+ with `dnslib`, `ipaddress`, and `requests`. Place `whoami.py` a preferred location, then modify `whoami.service` accordingly and copy to `/etc/systemd/system/`.

## About this project

The whoami script was first written in September 2015 for my client services team, which was having trouble diagnosing customer complaints. Some of the products we offered included geolocational routing for DNS, which sends visitors to different servers based on their location. For example, a visitor in New England could be routed to a server in Boston, while a visitor in California could be directed to a server in Sunnyvale. However, customers were reporting odd routing behavior from their tests, which we couldn’t adequately troubleshoot due to the number of variables.

Brief explainer: When someone performs a DNS lookup, their request is usually forwarded to a local or public resolver, such as Comcast, Google, etc., which then continues performing the legwork for the query. This prevents the target servers from responding to millions of individual requests. This is usually completely transparent to the user, which is where issuess arise: sometimes a local resolver is overriding the expected query path and getting a "wrong" result.

To help diagnose these problems, I created this pseudo-resolver. Unlike a regular resolver, whoami returns A, AAAA, and TXT records containing the IP address of the inbound request. This allowed customers to positively identify the last resolver in a chain; if they were in California but the final resolver's IP was in Boston, that usually meant they were funneling requests through their VPN at the home office elsewhere and getting these unexpected results.

Example:

```
~$ curl ifconfig.co -4          # my IP
73.249.238.143
~$ dig whoami.dyn.com +short    # my resolver’s IP
69.252.230.195
~$ dig -x 69.252.230.195 +short # my resolver’s identity
chlm-cns02.nlb.bos1.comcast.net.         
```

This sample is an earlier iteration of the pseudo-resolver, with added comments to explain the individual portions. It was eventually Dockerized for easy push-button deployment, and further changes were made to the log storage, but the core program is featured here.
