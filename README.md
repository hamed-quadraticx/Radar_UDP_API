# Radar_UDP_API
this API for the isys5020 radar, it used to receive and parse the incoming target list via Ethernet interface 

#steps:
1. install the HW connect configuration UART port and connect the UTP cable
2. before run API tester udp.py file you have to configure the radar to start acqustion via ethernet interface, you do this step by run UART API tester, you can fin it in  radar_API repo
3. after the configuration step was finished successfully run the UDP.py file 
4. the tester app is so simple, it is a multi process application starts a process to listen to the radar UDP port which was configured before
5. another  process will start immediatly will close the application after 20 seconds
6. target list will be logged on a text file
7. to run anoher test re do the previouse steps 


Thats all:)

