# 
# Server side code
#
# Simple Loopback Service Protocol
#
# ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_server.py
#

import struct
import logging

from aioquic.asyncio import QuicConnectionProtocol
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived

#
# configuration functions for server.py
#

def get_protocol_class():
    return SimpleLoopbackServerProtocol

def get_protocol_name():
    return 'Simple Loopback over QUIC' 

def get_protocol_alpn():
    return 'slboq'

#
# simple loopback service protocol code @ here 
#

class SimpleLoopbackServerProtocol(QuicConnectionProtocol): 

    def quic_event_received(self, event: QuicEvent):

        if isinstance(event, StreamDataReceived):
            
            # unpack query
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            data = event.data[2 : 2 + length]
            
            # do something
            logging.info('[strm:{}] {}'.format(
                event.stream_id,
                data
            ))

            # pack query result
            data = struct.pack("!H", len(data)) + data

            # send answer
            self._quic.send_stream_data(event.stream_id, data, end_stream=True)
            self.transmit()

#
# QUIC Evnets ?
#
# ref: https://aioquic.readthedocs.io/en/latest/quic.html#module-aioquic.quic.events 
# ref: https://github.com/aiortc/aioquic/blob/main/src/aioquic/quic/events.py
# 

#
# pack ?
#
# struct.pack() converts between Python values and C structs represented as Python bytes objects
# ref: https://docs.python.org/3/library/struct.html 
#
# ! means network (= big-endian)
# ref: https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment
#
# H means unsigned short in C
# ref: https://docs.python.org/3/library/struct.html#format-characters 
#
