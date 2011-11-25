#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A sample program that sends messages to the system.
"""

import json
import zmq
from conf import *


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(in_address)


for i in range(10):
    header = json.dumps({"mime-type": "text/plain"})
    msg = header + '\0' + "m%i" % i
    # OR msg = PlaintextObject("m%i" % i).bytes()!

    socket.send(msg)
    print "<< %s" % msg

    from_msg = socket.recv()
    print ">> %s" % from_msg
