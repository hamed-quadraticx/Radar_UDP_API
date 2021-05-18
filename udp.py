#imports
import logging
import multiprocessing
import threading
import socket
import sys
import time
from datetime import datetime
from target_list_header import Target_List_Header
from target_Data_Packet import Target_Data_Packet, Target_Data


logging.basicConfig(format='%(levelname)s - %(asctime)s : %(message)s',datefmt='%H:%M:%S',level=logging.DEBUG)
now = datetime.now()
log_file_name='targetList_'+str(now)+'.txt'
print("file name =", log_file_name)
log_file_obj = open(log_file_name, "x")
log_file_obj.write("Target list :")
#Socket
def make_socket(ip='localhost',port=2045,sender=False):
    proc = multiprocessing.current_process().name
    logging.info(f'{proc} : starting...')

    #  Define socket which will be using ipv4 and udp protocol
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    logging.info(f'{proc} : init socket...')
    if sender :
        logging.info(f'{proc}: stating to send ...')
    else:
        logging.info(f'{proc}: binding to port ...')
        address = (ip,port)
        s.bind(address)
        
        


    with s:
        while   True:
            logging.info(f'{proc}: loop ...')
            if sender:
                logging.info(f'{proc}: sending ...')
                s.sendto(b'0x1,0x2,0x3',(ip,port))
                time.sleep(1)
            else :
                data , addr = s.recvfrom(1024)
                logging.info(f'{proc}: received from {addr} = {(" , ".join(format(x, "02x") for x in data))} ')
                log_file_obj.write("\n")
                log_file_obj.write(f'{str(datetime.now())} : received from {addr} = \n {(" , ".join(format(x, "02x") for x in data))}')
                obj = Target_List_Header(data)
                chk = obj.parse()
                
                if chk is True and obj.no_of_packets > 0 and obj.no_of_targets >0 :
                    for x in range(obj.no_of_packets):
                        data , addr = s.recvfrom(1024)
                        logging.info(f'{proc}: received from {addr} = {(" , ".join(format(x, "02x") for x in data))} ')
                        log_file_obj.write("\n")
                        log_file_obj.write(f'{str(datetime.now())} : received from {addr} = \n {(" , ".join(format(x, "02x") for x in data))}')
                        data_packet = Target_Data_Packet(obj.frame_id,obj.no_of_packets, obj.no_of_targets, data)
                        data_packet.parse()
                        log_file_obj.write("\n")
                        log_file_obj.write("Parsed Target data :")
                        targe_id = 0
                        for _target in  data_packet.targets_list:
                            target_id = targe_id+1
                            log_file_obj.write(f'\n Target ID ={targe_id} \n RCS ={_target.signal_strength} \n range = {_target.range} \n  velocity ={_target.velocity} \n angle= {_target.angle_azimuth}')

     
                    



                
                

# main func
def main():
    logging.info(f' main ...')
    #broadcaster  = multiprocessing.Process(target=make_socket,kwargs={'sender':True}, daemon= True,name ='Radar')
    listener  = multiprocessing.Process(target=make_socket,kwargs={'ip':'192.168.1.20','port':2050,'sender':False}, daemon= True,name ='listener')
    
    #broadcaster.start()
    listener.start()
    
    timer = threading.Timer(20,app_exit)
    timer.start()

def app_exit():
    log_file_obj.close()
    sys.exit([0])


if __name__ == "__main__":
    main()





