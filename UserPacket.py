#!/usr/local/bin/python3
# -*- coding: utf8 -*-

import sys
import ctypes
import socket
from ctypes import * c_ushort, c_ubyte, c_uint8, c_double

IP = "127.0.0.1"
PORT = 5010

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SEND
sock.connect((IP, PORT))

class ip_address(Structure):
    _fields_ = [("byte1", u_char),
                ("byte2", u_char),
                ("byte3", u_char),
                ("byte4", u_char)]


class ip_header(BigEndianStructure):
    _fields_ = [("ver_ihl", u_char),
                ("tos", u_char),
                ("tlen", u_short),
                ("identification", u_short),
                ("flags_fo", u_short),
                ("ttl", u_char),
                ("proto", u_char),
                ("crc", u_short),
                ("saddr", ip_address),
                ("daddr", ip_address),
                ("op_pad", u_int)]


class udp_header(BigEndianStructure):
    _fields_ = [("sport", u_short),
                ("dport", u_short),
                ("len", u_short),
                ("crc", u_short)]
				
class ROBOT_JOINT_REF(Structure):
	_pack_ = 1
	_fields_ = [("pos",c_double),
		   ("velocity",c_double),
		   ("acc",c_double),
		   ("mode",c_uint8),
		   ("ID",c_uint8),
		   ("lammbda",c_double),
		   ("cmd",c_double)]


def packet_handler(pkt_data):

    # cast pkt_data to void so we can do some pointer arithmetic
    v_pkt_data = ctypes.cast(pkt_data, ctypes.c_void_p)

    # retrieve the position of the ip header
    v_ip_header = ctypes.c_void_p(v_pkt_data.value + 14)
    pih = ctypes.cast(v_ip_header, ctypes.POINTER(ip_header))
    ih = pih.contents

    # retrieve the position of the udp header
    ip_len = (ih.ver_ihl & 0xf) * 4
    uh = ctypes.cast(ctypes.cast(pih, ctypes.c_void_p).value + ip_len,
                     ctypes.POINTER(udp_header)).contents

    # convert from network byte order to host byte order
    sport = socket.ntohs(uh.sport)
    dport = socket.ntohs(uh.dport)

    print("{}.{}.{}.{}:{} -> {}.{}.{}.{}:{}".format(
        ih.saddr.byte1, ih.saddr.byte2, ih.saddr.byte3, ih.saddr.byte4, sport,
        ih.daddr.byte1, ih.daddr.byte2, ih.daddr.byte3, ih.daddr.byte4, dport))

    # Extracting data
    #

    # data offset from ip header start
    data_offset = ip_len + ctypes.sizeof(udp_header)
    # data length
    data_len = ih.tlen - ip_len - ctypes.sizeof(udp_header)
    # get data
    arr_type = (ctypes.c_uint8 * data_len)
    data = arr_type.from_address(v_ip_header.value + data_offset)

    print(data[0:data_len])

    # note: same thing could be achieved from pkt_data
    print(pkt_data[14+data_offset:14+data_offset+data_len])


def main(packet_file):
    with open(packet_file, "rb") as fd:
        data = fd.read()

    # create ctypes.c_char_array
    pkt_data = ctypes.c_buffer(data)
    packet_handler(pkt_data)

maxval = 1
minval = 0

getmsg = '0'
setmsg = '1'

pos = '0001'
velos = '0010'
acc = '0011'
mode = '0100'
ID = '0101'
lammbda = '0110'
cmd = '0111'
#torque = '1000'
#maxtorque = '1001'
#motID = '1010'

def getval(msg):
	packet = getmsg + msg
	sock.send(packet)
	print 'sent: ', packet
	data = sock.recv(1024)
	return int(data,2)

def setval(msg, val):
	if (val > maxval):
		val = maxval
	if (val < minval):
		val = minval
	value = val*15
	packet = setmsg + msg + bin(value)
	sock.send(packet)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    while(True):
	msgtype = input("Get (0) or Set(1)")
	msgvar = input("enter variable(vel = 0001, acel = 0010, etc): ")
	if msgvar == 0001:
		msg = pos
	if msgvar == 0010:
		msg = velocity
	if msgvar == 0011:
		msg = acc
	if msgvar == 0100:
		msg = mode
	if msgvar == 0101:
		msg = ID
	if msgvar == 0111:
		msg = lammbda
	if msgvar = 0111:
		msg = cmd
	#if msgvar = 1000:
	#	msg = torque
	#if msgvar = 1001:
	#	msg = maxtorque
	#if msgvar = 1010
	#	msg = motID

	if (msgtype == 0):
		print "received: ", getval(msg)
	if (msgtype == 1):
		msgvalue = input("enter value: ")
		setval(msg,msgvalue)
	time.sleep(.01)
