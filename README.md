Battlefield: Bad Company 2 Master Server Emulator
=================================================

![Battlefield: Bad Company 2 Cover](https://upload.wikimedia.org/wikipedia/en/b/b3/Battlefield_Bad_Company_2_cover.jpg "Battlefield: Bad Company 2 Cover")


Game Info
---------

Type         | Value
------------:|:-----------
Developer(s) | EA DICE
Publisher(s) | Electronic Arts
Writer(s)    | David Goldfarb
Composer(s)  | Mikael Karlsson, Joel Eriksson
Series       | Battlefield
Engine       | Frostbite 1.5
Platform(s)  | Microsoft Windows, PlayStation 3, Xbox 360, iOS, Kindle Fire
Genre(s)     | First-person shooter
Mode(s)      | Single-player, Multi-Player


Legal notes
-----------

- The project aren't containing *any* of the original code from the game!!! 
- It is an emulated program!
- That are imitating original server
- It is completely legal to use this code!
 

Requirements
------------

- Original copy of Battlefield: Bad Company 2

Module           | Version | Download
----------------:|:-------:|:------------
Python           | 2.7     | [Python Download](https://www.python.org/)
colorama         | latest  | pip install colorama
passlib          | latest  | pip install passlib
Twisted          | 16.3.0  | pip install Twisted==16.3.0
pyOpenSSL        | 0.15.1  | pip install pyOpenSSL==0.15.1
cffi             | 1.3.0   | pip install cffi==1.3.0
cryptography     | 0.7.2   | pip install cryptography==0.7.2
service_identity | 1.0.0   | pip install service_identity==1.0.0

*...or just install everything via `pip install -r requirements.txt`*

Also you have to open these ports:

Port   | Type
------:|:-------
18390  | TCP
18395  | TCP/UDP
19021  | TCP
19026  | TCP/UDP


Setting up the emulator
-----------------------

- Make sure that all required ports (see above) are open
- Write the IP of the PC where the emulator will be hosted in the config.ini to the key 'emulator_ip' (overwrite "REPLACE_ME") and save it
- Run `Init.py`

Setting up Client and Server
----------------------------

There are 2 different methods you can choose from to set them up

1. Using the dinput8.dll hook

1.1. Simply put the "dinput8.dll" file in the root directory of the Client/Server (where the executable is located)

2. Manually modifying the binaries and redirect the IP's over the hosts file

2.1. First remove the SLL verification of the executable by using the lame patcher tool (http://aluigi.altervista.org/mytoolz/lpatch.zip) with the fesl patch (http://aluigi.altervista.org/patches/fesl.lpatch)

2.2. Add this to your hosts file:

    # redirect client ip's
    xxx bfbc2-pc.fesl.ea.com
    xxx bfbc2-pc.theater.ea.com
    # redirect server ip's
    xxx bfbc2-pc-server.fesl.ea.com
    xxx bfbc2-pc-server.theater.ea.com
    # optional
    xxx easo.ea.com

*Where 'xxx' stands for the IP of the PC that hosts the emulator.*

Credits
-------

- B1naryKill3r (Main Programmer/Developer)

Special thanks to:
- Domo and Freaky123 (for sharing the Server Files and the v10.0 source code)
- DICE (for making the game)
