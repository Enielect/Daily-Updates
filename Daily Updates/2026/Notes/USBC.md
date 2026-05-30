Today (Right now it is 10:37) and our topic of concern for today in our quest to get a little better at electronics and RF (telecommunications engineering). We are going to be learning about the USBC. We have only 1:30 mins of today to treat this topic.

What are TID listed products in USB? What does it mean when they say that we cannot use the USB logo unless we pay for TID?

USB 1.0, 1.1, 2.0, 3.0 (support power application with phones and batteries. It can delivered 5V at 1.5 A), 3.1 (Delivered 20V at 5A)

The type C is a connector using the USB 3.1 standard
Take note that there are connectors (the male), and there are interfaces (female)
The Type C connector is not a new interface, it is just a new cable and connector definition where you can run different existing protocols. E.g you can run the usb 2.0, 3.0, 3.1, 3.2, thunderbolt, hdmi, 4.0, power, audio e.t.c


#### Learning about pinging. (Mon 18 May 2026)
Ping is a term derived from sonar technology where pulses of sound are sent, while we listens for the echo to return.

We can use this package to send several packets to a specified IP or domain either on our local network or on the internet.
`ping <IP|domain>`

- This process resolves the IP address, if we had inputed the a url.
It tells how the time it took for the packet to go to the destinatino server and return. It also reveals the (TTl) time to live of the packet.
    - We can use a tool called [traceroute](https://dnschecker.org/online-traceroute.php) to map the route that packets take from hour device to a destination IP or domain. It also helps tell the RTT(Round-trip time) for backets to reach each hop and return. 

- To troubleshoot a failed ping:
    - ping your router if you can't reach an internet location. (A successful ping lets you know that your local network is working okey)
    - Ping your loopback address (127.0.0.1) if you can't successfully ping your router. A successful ping lets you know that your network adapter on your computer is working properly.

### Downloading from the Ubuntu repository (Note that PPA are not official):
A Personal Package Archive (PPA) is a third-party software repository hosted on Launchpad that allows individual developers and users to distribute software packages for Ubuntu and other Debian-based Linux distributions.  Unlike official repositories, which are maintained by the distribution's developers and undergo rigorous testing, PPAs provide unofficial access to newer software versions, experimental builds, or packages not included in the standard distribution channels.

Users can easily add a PPA using the `add-apt-repository` command and install software via the APT package manager, just like official packages


