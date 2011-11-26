#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A sample program that listens to the listening port.
"""

import zmq
from conf import *

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE,'')
socket.connect(out_address)

while True:
    msg = socket.recv()
    print ">> %s" % msg
