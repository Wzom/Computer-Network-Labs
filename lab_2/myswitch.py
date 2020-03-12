'''
Ethernet learning switch in Python.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.userlib import *

def main(net):
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]

    while True:
        try:
            timestamp,input_port,packet = net.recv_packet()
        except NoPackets:
            log_info("Hit except NoPackets.")
            continue
        except Shutdown:
            log_info("Hit except Shutdown.")
            return

        log_info("In {} received packet {} on {}".format(net.name, packet, input_port))
        if packet[0].dst in mymacs:
            log_info("Packet intended for me")
        else:
            for intf in my_interfaces:
                if input_port != intf.name:
                    log_info("Flooding packet {} to {}".format(packet, intf.name))
                    net.send_packet(intf.name, packet)
    net.shutdown()
