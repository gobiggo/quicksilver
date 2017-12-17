# quicksilver
A man-in-the-middle tool styled after the NSA's "quantum insert" method of gaining access to a target device.
Current (Version 1) Capabilities:
  Standard MITM tool capable of reading client packets and use of tools such as urlsnarf and driftnet
Next update (Version 2) plans:
  -A far grittier update which manually spoofs arp and forwards packets with in-house SCAPY code
  -Writing packets to a specified log file automatically -l 
  -Taking it off manual code insertion ([\*] Please Specify Target:) to replace with flags (-t target)
  -Possibility of GUI -g
Version 3 plans:
  -Webpage substitution (Deliver to a local-page rather than the regular page)
  -Insertion of specified javascript with -p /path/to/payload.js
  -User-made modules?
Assorted plans:
  -Awesome loading banner
NOTE: Not all developed versions are necessarily on this repository.
