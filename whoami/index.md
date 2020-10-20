## README

[whoami.py](https://github.com/jhutchinsnh/jhutchinsnh.github.io/tree/master/whoami) requires Python 2.7+ with `dnslib`, `ipaddress`, and `requests`. Place `whoami.py` a preferred location, then modify `whoami.service` accordingly and copy to `/etc/systemd/system/`.

## About this project

The first artifact for my portfolio is whoami. The whoami script was written in September 2015 for my company’s client services team, which was having trouble diagnosing customer complaints. Some of the products we offer include geolocational routing for DNS, which sends visitors to different servers based on their location. For example, a visitor in New England could be routed to a server in Boston, while a visitor in California could be directed to a server in Sunnyvale. However, customers were reporting odd routing behavior from their tests, which we couldn’t adequately troubleshoot due to the number of variables.

To help diagnose these problems, I wrote whoami, which is a pseudo-resolver. Unlike a regular resolver, whoami returns A, AAAA, and TXT records containing the IP address of the inbound request. When a customer tries a DNS lookup against it, they’re able to see where their query is actually coming from, which solves a lot of the guesswork. With this tool, we were able to prove that the problems lay on the customers’ end; the majority of the trouble turned out to be a misunderstanding of VPNs, which were causing “local” requests to be routed out to companies’ main offices across the country, causing them to receive the wrong answer.

I included this artifact for the Software Design and Engineering artifact because it’s one of my longest-running and most-used troubleshooting tools for our support staff. In fact, it’s still running and accessible now: performing dig whoami.dyn.com will return a valid DNS response that contains your resolver’s IP address. For instance, while I’m in New Hampshire, whoami demonstrates that I’m actually sending DNS requests out of Comcast's resolver in Boston:

```
~$ curl ifconfig.co -4          # my IP
73.249.238.143
~$ dig whoami.dyn.com +short    # my resolver’s IP
69.252.230.195
~$ dig -x 69.252.230.195 +short # my resolver’s identity
chlm-cns02.nlb.bos1.comcast.net.         
```

However, I’d written the tool under time constraints, and simply never had an opportunity to go back and correct some of the mistakes I’d made. For instance, instead of running the script as a background process, I simply let it run in the foreground in a screen forever, which is a very hacky method. There were also minor inconsistencies, the comments were fairly lackluster, and a number of options were hardcoded (e.g. the default hostname). I’ve also learned a lot more about Python in the last five years, so I knew I could improve the script in general by just giving it a once-over.

To improve the artifact, I first went through the code line by line and added commentary to properly explain what each piece did. When I’d written it initially, each block seemed fairly obvious, but coming back years later made it difficult to decipher certain decisions (e.g. why some responses included DNS authority sections and others didn’t). This re-familiarized me with the project and allowed me to spot errors in one of the edge cases. Further improvements include better error handling for permissions issues and more visually useful logging formats. I also took the time to reformat Python print statements to use the newer .format instead of % replacements.

The big change was creating a service script that would allow anyone to run the pseudo-resolver via systemd, courtesy of systemctl. Operating as a system service is a much cleaner and common-sense method for hosting a permanent background process, while also ensuring the proper parameters are supplied on each start-up. This greatly simplifies troubleshooting for other engineers, who can simply restart the process instead of identifying the screen session, terminating it and its child processes, and making a whole new screen. It’s something I’ve wanted to do to improve the script for a long time, and I’m glad I’ve now learned how to run Python scripts as system services. I’ve also learned how to interact with system signals and handlers in Python like SIGTERM to appropriately address them.

I was interested in possibly running the service as a Docker container, but ultimately decided that was overkill. Python is a well-supported programming language, and the packages required for the script are fairly lightweight and common. It’s much more likely a given server will support Python over Docker, as it needs no esoteric configuration.

In all, I’m quite happy with the work I was able to put in to polish an old script that’s still seeing active use. At the next opportunity, I’ll be upgrading the tiny server housing the current script at whoami.dyn.com with the new code, and likely assessing the server itself for up-to-date security patches.
