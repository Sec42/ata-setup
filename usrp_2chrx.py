#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Usrp 2Chrx
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq

class usrp_2chrx(gr.top_block):

    def __init__(self, fc=629e6, gaindB=23, samp_rate=12.5e6):
        gr.top_block.__init__(self, "Usrp 2Chrx")

        ##################################################
        # Parameters
        ##################################################
        self.fc = fc
        self.gaindB = gaindB
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.chans = chans = 4096

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, chans, 'tcp://*:50001', 100, False, -1)
        self.uhd_usrp_source = uhd.usrp_source(
            ",".join(("addr=10.11.2.61", "master_clock_rate=250e6")),
            uhd.stream_args(
                cpu_format="fc32",
                otw_format="sc16",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source.set_subdev_spec('A:0 B:0', 0)
        self.uhd_usrp_source.set_time_source('external', 0)
        self.uhd_usrp_source.set_clock_source('external', 0)
        self.uhd_usrp_source.set_center_freq(fc, 0)
        self.uhd_usrp_source.set_gain(gaindB, 0)
        self.uhd_usrp_source.set_antenna('TX/RX', 0)
        self.uhd_usrp_source.set_center_freq(fc, 1)
        self.uhd_usrp_source.set_gain(gaindB, 1)
        self.uhd_usrp_source.set_antenna('TX/RX', 1)
        self.uhd_usrp_source.set_samp_rate(samp_rate)
        self.uhd_usrp_source.set_time_unknown_pps(uhd.time_spec())
        self.fft_vxx_0_0 = fft.fft_vcc(chans, True, window.blackmanharris(chans), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(chans, True, window.blackmanharris(chans), True, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, chans)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, chans)
        self.blocks_interleave_0 = blocks.interleave(gr.sizeof_float*chans, 1)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(1000, chans)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(1000, chans)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(chans)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(chans)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_interleave_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_interleave_0, 1))
        self.connect((self.blocks_interleave_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.uhd_usrp_source, 1), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.uhd_usrp_source, 0), (self.blocks_stream_to_vector_0_0, 0))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_source.set_center_freq(self.fc, 0)
        self.uhd_usrp_source.set_center_freq(self.fc, 1)

    def get_gaindB(self):
        return self.gaindB

    def set_gaindB(self, gaindB):
        self.gaindB = gaindB
        self.uhd_usrp_source.set_gain(self.gaindB, 0)
        self.uhd_usrp_source.set_gain(self.gaindB, 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source.set_samp_rate(self.samp_rate)

    def get_chans(self):
        return self.chans

    def set_chans(self, chans):
        self.chans = chans


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--fc", dest="fc", type=eng_float, default="629.0M",
        help="Set carrier frequency [default=%(default)r]")
    parser.add_argument(
        "-g", "--gaindB", dest="gaindB", type=eng_float, default="23.0",
        help="Set rx gain in decibels [default=%(default)r]")
    parser.add_argument(
        "-b", "--samp-rate", dest="samp_rate", type=eng_float, default="12.5M",
        help="Set sampling rate [Hz] [default=%(default)r]")
    return parser


def main(top_block_cls=usrp_2chrx, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(fc=options.fc, gaindB=options.gaindB, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
