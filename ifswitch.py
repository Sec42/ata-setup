#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ifswitch
# GNU Radio version: 3.8.1.0

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import ata

class ifswitch(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "ifswitch")

        ##################################################
        # Blocks
        ##################################################
        self.ata_trackscan_0 = ata.trackscan(1622.0, '1h', 'azel')
        self.ata_trackscan_0.set_src_azel(90.0, 25)
        self.ata_ifswitch_0 = ata.ifswitch('none', '1h', 'none')
        self.ata_control_0 = ata.control('gnuradio', 'online')



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ata_trackscan_0, 'command'), (self.ata_control_0, 'command'))



def main(top_block_cls=ifswitch, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
