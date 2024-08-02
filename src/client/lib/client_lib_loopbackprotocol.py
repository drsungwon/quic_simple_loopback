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
import time

from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived

#
# configuration functions for server.py
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
        for count in range(1,6):
            time.sleep(2)
            msg = 'hello #' + str(count)
            await self.send_loopback_msg(str(msg))
        return 

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self._ack_waiter = None

    async def send_loopback_msg(self, msg: str) -> None:

        # make message to send
        data = bytes(msg, encoding='utf8')
        data = struct.pack("!H", len(data)) + data

        # send message 
        self.stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(self.stream_id, data, end_stream=True)
        
        # regist async wait for answer
        waiter = self._loop.create_future() # fyi: _loop is asyncio.get_event_loop()
        self._ack_waiter = waiter
        self.transmit()
        await asyncio.shield(waiter) 

    def quic_event_received(self, event: QuicEvent) -> None:

        if isinstance(event, StreamDataReceived):

            # parse answer
            length = struct.unpack("!H", bytes(event.data[:2]))[0]
            msg = event.data[2 : 2 + length]

            # do something
            logging.info("quic_event_received(): {}".format(msg))

            # finish the registered asyncio.Future
            if self._ack_waiter is not None:
                waiter = self._ack_waiter
                self._ack_waiter = None
                waiter.set_result(msg) 
                logging.info("quic_event_received(): waiter released")

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

#
# concurrency code summary
#
# r = asyncio.get_event_loop()	
#     Get the current event loop.
#     https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop
#     use asyncio.run()
# 
# r.create_future()				
#     Create an asyncio.Future object attached to the event loop.
#     https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_future
# 
# asyncio.shield(r)
#     Protect an awaitable object from being cancelled.
#     https://docs.python.org/3/library/asyncio-task.html#asyncio.shield
# 
# r.set_result()
#     Mark the Future as done and set its result.
#     https://docs.python.org/3/library/asyncio-future.html#asyncio.Future.set_result
# 
