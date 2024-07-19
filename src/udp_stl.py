# get TRex APIs
import lbr_trex_client
from trex.stl.api import *
from trex.astf.api import *
from trex_stl_lib.api import *
from trex_client import CTRexClient
from trex_exceptions import TRexInUseError
from scapy.layers.dns import *

# import stl_path                                                         1
# from trex_stl_lib.api import *

import time
import json

# simple packet creation
def create_pkt (siz):
    vm = [
        # src
        STLVmFlowVar(name="src", min_value="192.168.120.2", max_value="192.168.120.254", size=4, op="inc"),
        STLVmWrFlowVar(fv_name="src",pkt_offset= "IP.src"),
        # checksum
        STLVmFixIpv4(offset = "IP")
    ]
    base = Ether()/IP()/UDP(dport=10000)
    pad = (siz-len(base)) * 'x'
    return STLPktBuilder(pkt = base/pad, vm  = vm)

def create_ARP_request_gratuituous():
    vm = [
        # src
        STLVmFlowVar(name="src", min_value="192.168.120.2", max_value="192.168.120.254", size=4, op="inc"),
        STLVmWrFlowVar(fv_name="src",pkt_offset= "28"),
        # checksum
        STLVmFixIpv4(offset = "IP")
    ]
    arp = ARP(psrc="192.168.120.2",
              hwsrc='14:02:ec:79:f0:34',
              pdst="192.168.120.2")

    return STLPktBuilder(pkt = Ether(dst='ff:ff:ff:ff:ff:ff') / arp, vm  = vm)
    

def simple_burst ():

    c = STLClient()
    passed = True

    try:
        # turn this on for some information
        #c.set_verbose("high")

        s1 = STLStream(packet = create_pkt(64), mode = STLTXCont(pps = 1))

        # connect to server
        c.connect()

        # prepare our ports (my machine has 0 <--> 1 with static route)
        c.reset(ports = [0]) #  Acquire port 0,1 for $USER 

        c.add_streams(s1, ports = [0])

        # clear the stats before injecting
        c.clear_stats()
        
        m="16mpps"
        d=60
        # choose rate and start traffic for 10 seconds on 5 mpps
        print(f"Running {m} on ports 0 for {d} seconds...")
        c.start(ports = [0], mult = m, duration = d, force=True)

        # block until done
        c.wait_on_traffic(ports = [0])

        # read the stats after the test
        stats = c.get_stats()

        # print(json.dumps(stats[0], indent = 4, separators=(',', ': '), sort_keys = True))
        # print(json.dumps(stats[1], indent = 4, separators=(',', ': '), sort_keys = True))

        lost_a = stats[0]["opackets"] - stats[0]["ipackets"]

        print("\npackets lost from 0 --> 1:   {0} pkts".format(lost_a))

        if (lost_a == 0) :
            passed = True
        else:
            passed = False

    except STLError as e:
        passed = False
        print(e)

    finally:
        c.disconnect()

    if passed:
        print("\nTest has passed :-)\n")
    else:
        print("\nTest has failed :-(\n")


# run the tests
simple_burst()