# 
# Client side code
#
# Simple Loopback Service Protocol
#
# ref: https://github.com/aiortc/aioquic/blob/main/examples/doq_client.py
#

import asyncio
import struct
import logging

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived

#
# configuration functions for client.py
#

def get_protocol_class():
    return SimpleLoopbackClientProtocol

def get_protocol_name():
    return 'Simple Loopback over QUIC' 

def get_protocol_alpn():
    return 'slboq'

#
# simple loopback service protocol code @ here 
#

class SimpleLoopbackClientProtocol(QuicConnectionProtocol):

    async def activate_protocol(self) -> None:
        '''
        Callback which is invoked by the client.py when a client program is executed
        '''
        for count in range(0,20):
            await asyncio.sleep(2)
            msg = 'hello #' + str(count+1)
            await self.send_loopback_msg(str(msg))

    async def send_loopback_msg(self, msg: str) -> None:

        # make message to send
        data = bytes(msg, encoding='utf8')
        data = struct.pack("!H", len(data)) + data

        # send message 
        self.stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(self.stream_id, data, end_stream=True)
        self.transmit()
        logging.info("send_loopback_msg(): {} sent".format(msg))

    def quic_event_received(self, event: QuicEvent) -> None:

        if isinstance(event, StreamDataReceived):
            # parse answer
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            msg = event.data[2 : 2 + length]
            logging.info("quic_event_received(): {}".format(msg))

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

