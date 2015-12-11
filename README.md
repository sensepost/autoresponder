"Auto-Responder"
==========

This project is highly inspired from [Autoresp](https://github.com/DanMcInerney/autoresp) from Dan McInerney. Check out his project. 

The aim of this python script is to run in addition with [Responder](https://github.com/SpiderLabs/Responder) while doing internal assessments. 
This script will monitor the logs from Responder, loads NTLMv1 and NTLMv2 on the fly and crack them with your instance of Hashcat. Locally. 

Works out of the box on Kali Linux (including 2.0)

Installation
==========

Clone the repo: 

```git clone <repo> && cd autoresponder```

And.. you're done. 

Usage
==========

The command ```python auto_responder.py -h``` will actually show you this usage: 

```
python auto_responder.py -h
usage: auto_responder.py [-h] [-w WORDLIST] [-l LOGS_DIR] [-b HASHCAT_PATH]
                         [-a HASHCAT_ARGS]

Auto Responder - @PaulWebSec (SensePost)

optional arguments:
  -h, --help       show this help message and exit
  -w WORDLIST      Path to the worlists. eg. /wordlists/*.txt
  -l LOGS_DIR      Path to Responder binary (default: /usr/share/responder)
  -b HASHCAT_PATH  Path to Hashcat binary (default: /usr/bin/hashcat)
  -a HASHCAT_ARGS  Arguments to pass to hashcat. eg. "-r
                   /usr/share/hashcat/rules/best64.rule"
  ```

Parameters **logs_dir** and **hashcat_path** are not mandatory. Defaults are Kali ones. 
The only mandatory parameter is the **wordlist** one. 

```
python auto_responder.py -w '/usr/share/wordlists/metasploit/*'
48 NTLMv2 hashes loaded.
2 NTLMv1 hashes loaded.
[!] Cracked NTLMv2 hash: SMB12\ADMIN:password (172.16.93.1)
[!] Cracked NTLMv2 hash: WORKGROUP\ROOT: (172.16.93.132)
[!] Cracked NTLMv2 hash: SMB12\GUEST: (172.16.93.1)
```

As soon as you launch the script, it will retrieve all the hashes stored in the logs folder and start bruteforcing them.

Contributing
==========

I developped this script in few hours, which means it might contains bugs. 
For new features ping me on Twitter [@PaulWebSec](https://twitter.com/PaulWebSec)