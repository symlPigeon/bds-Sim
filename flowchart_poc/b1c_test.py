#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: syml
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from hier_b1c_boc import hier_b1c_boc  # grc-generated hier_block
import math



from gnuradio import qtgui

class b1c_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "b1c_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_0 = samp_rate_0 = 6.138e6*8
        self.samp_rate = samp_rate = 6.138e6*8
        self.pilot_sps = pilot_sps = 1.023e6
        self.f_sc_b1c_b = f_sc_b1c_b = 6.138e6
        self.f_sc_b1c_a = f_sc_b1c_a = 1.023e6
        self.data_sps = data_sps = 100

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.hier_b1c_boc_0 = hier_b1c_boc(
            data_sps=100,
            delay=0,
            f_sc_b1c_a=1.023e6,
            f_sc_b1c_b=(1.023e6 * 6),
            pilot_sps=1.023e6,
        )
        self.analog_random_uniform_source_x_0_0_0 = analog.random_uniform_source_b(0, 2, 0)
        self.analog_random_uniform_source_x_0_0 = analog.random_uniform_source_b(0, 2, 0)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 2, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.hier_b1c_boc_0, 0))
        self.connect((self.analog_random_uniform_source_x_0_0, 0), (self.hier_b1c_boc_0, 2))
        self.connect((self.analog_random_uniform_source_x_0_0_0, 0), (self.hier_b1c_boc_0, 1))
        self.connect((self.hier_b1c_boc_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "b1c_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pilot_sps(self):
        return self.pilot_sps

    def set_pilot_sps(self, pilot_sps):
        self.pilot_sps = pilot_sps

    def get_f_sc_b1c_b(self):
        return self.f_sc_b1c_b

    def set_f_sc_b1c_b(self, f_sc_b1c_b):
        self.f_sc_b1c_b = f_sc_b1c_b

    def get_f_sc_b1c_a(self):
        return self.f_sc_b1c_a

    def set_f_sc_b1c_a(self, f_sc_b1c_a):
        self.f_sc_b1c_a = f_sc_b1c_a

    def get_data_sps(self):
        return self.data_sps

    def set_data_sps(self, data_sps):
        self.data_sps = data_sps




def main(top_block_cls=b1c_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
