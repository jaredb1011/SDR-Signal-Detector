#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Peak Detector
# Author: Jared Boggs, Christopher Nguyen, Seth Graham, Matthew Buker
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import correctiq
import epy_block_0
import epy_block_1
import osmosdr
import time
import os
from multiprocessing import shared_memory
from gnuradio import qtgui
import numpy as np

class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Peak Detector")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Peak Detector")
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
        self.fileName = "./output_files/out_file.sigmf-data"
        self.settings = Qt.QSettings("GNU Radio", "top_block")

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
        self.update_period = update_period = 0.10
        self.sys_enabled = sys_enabled = True
        self.samp_rate = samp_rate = 10e6
        self.peak_threshold = peak_threshold = 1.1
        self.peak_size = peak_size = 30
        self.peak_scale = peak_scale = 5
        self.fft_size = fft_size = 1024
        self.center_freq = center_freq = 93000000
        self.avg_window_size = avg_window_size = 120
        self.freqListRate = 500
        self.sethFreq = 0.0

        ##################################################
        # Blocks
        ##################################################
        _sys_enabled_check_box = Qt.QCheckBox('Enable')
        self._sys_enabled_choices = {True: False, False: True}
        self._sys_enabled_choices_inv = dict((v,k) for k,v in self._sys_enabled_choices.items())
        self._sys_enabled_callback = lambda i: Qt.QMetaObject.invokeMethod(_sys_enabled_check_box, "setChecked", Qt.Q_ARG("bool", self._sys_enabled_choices_inv[i]))
        self._sys_enabled_callback(self.sys_enabled)
        _sys_enabled_check_box.stateChanged.connect(lambda i: self.set_sys_enabled(self._sys_enabled_choices[bool(i)]))
        self.top_grid_layout.addWidget(_sys_enabled_check_box)
        self._peak_threshold_tool_bar = Qt.QToolBar(self)
        self._peak_threshold_tool_bar.addWidget(Qt.QLabel('Detection Threshold' + ": "))
        self._peak_threshold_line_edit = Qt.QLineEdit(str(self.peak_threshold))
        self._peak_threshold_tool_bar.addWidget(self._peak_threshold_line_edit)
        self._peak_threshold_line_edit.returnPressed.connect(
            lambda: self.set_peak_threshold(eng_notation.str_to_num(str(self._peak_threshold_line_edit.text()))))
        self.top_grid_layout.addWidget(self._peak_threshold_tool_bar, 2, 0, 1,2)
        self._peak_scale_tool_bar = Qt.QToolBar(self)
        self._peak_scale_tool_bar.addWidget(Qt.QLabel('Peak Scale' + ": "))
        self._peak_scale_line_edit = Qt.QLineEdit(str(self.peak_scale))
        self._peak_scale_tool_bar.addWidget(self._peak_scale_line_edit)
        self._peak_scale_line_edit.returnPressed.connect(
            lambda: self.set_peak_scale(eng_notation.str_to_num(str(self._peak_scale_line_edit.text()))))
        self.top_grid_layout.addWidget(self._peak_scale_tool_bar)
        self._center_freq_tool_bar = Qt.QToolBar(self)
        self._center_freq_tool_bar.addWidget(Qt.QLabel('Freq Selection' + ": "))
        self._center_freq_line_edit = Qt.QLineEdit(str(self.center_freq))
        self._center_freq_tool_bar.addWidget(self._center_freq_line_edit)
        self._center_freq_line_edit.returnPressed.connect(
            lambda: self.set_center_freq(int(str(self._center_freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._center_freq_tool_bar)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            fft_size,
            center_freq - (samp_rate/2),
            samp_rate/fft_size,
            'Frequency (hz)',
            'Peak Detected',
            "Peaks Detector",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(update_period)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 1.3)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)

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
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win, 4, 0, 3, 4)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_size,
            center_freq - (samp_rate/2),
            samp_rate/fft_size,
            'Frequency',
            'Relative Power',
            "FFT",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(update_period)
        self.qtgui_vector_sink_f_0.set_y_axis(-10, 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

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
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 7, 0, 3, 4)
        self.freqList = Qt.QListWidget(self) #THIS IS OUR ADDITION< THIS LINE RIGHT HERE< HERE IT IS
        self.durationLabel = Qt.QLabel("Duration:")
        self.durationLine = Qt.QLineEdit("3")
        self.rateLabel = Qt.QLabel("Sample Rate:")
        self.rateLine = Qt.QLineEdit("1000000")
        self.fileButton = Qt.QPushButton("Recording File Path")
        self.exportButton = Qt.QPushButton("Export List")
        self.top_grid_layout.addWidget(self.durationLabel,2,3, 1, 1)
        self.top_grid_layout.addWidget(self.durationLine,2,4, 1, 1)
        self.top_grid_layout.addWidget(self.rateLabel,3,3, 1, 1)
        self.top_grid_layout.addWidget(self.rateLine,3,4, 1, 1)
        self.top_grid_layout.addWidget(self.fileButton,4,4, 1, 1)
        self.top_grid_layout.addWidget(self.exportButton,5,4, 1, 1)
        self.top_grid_layout.addWidget(self.freqList, 6, 4, 6, 1)
        self.freqList.itemClicked.connect(self.sethFunction)
        self.fileButton.clicked.connect(self.setFilePath)
        self.exportButton.clicked.connect(self.saveList)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, window.blackmanharris(1024), True, 8)
        self.epy_block_1 = epy_block_1.blk(start_frequency=center_freq - (samp_rate/2), sample_rate=samp_rate, vector_size=fft_size)
        self.epy_block_0 = epy_block_0.blk(vector_size=fft_size)
        self.correctiq_correctiq_0 = correctiq.correctiq()
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, 1024)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, 1024)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,sys_enabled)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_peak_detector2_fb_0 = blocks.peak_detector2_fb(peak_threshold, peak_size, 0.001)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(1, fft_size, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(avg_window_size, peak_scale/avg_window_size, 4000, fft_size)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_peak_detector2_fb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.correctiq_correctiq_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_peak_detector2_fb_0, 0))
        self.connect((self.correctiq_correctiq_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_selector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_update_period(self):
        return self.update_period

    def set_update_period(self, update_period):
        self.update_period = update_period
        self.qtgui_vector_sink_f_0.set_update_time(self.update_period)
        self.qtgui_vector_sink_f_0_0.set_update_time(self.update_period)

    def get_sys_enabled(self):
        return self.sys_enabled

    def set_sys_enabled(self, sys_enabled):
        self.sys_enabled = sys_enabled
        self._sys_enabled_callback(self.sys_enabled)
        self.blocks_selector_0.set_output_index(self.sys_enabled)

    def get_samp_rate(self):
        return self.samp_rate

    def sethFunction(self, item):
        if (self.fileName == ""):
            print("\nNo directory selected, defaulted to './output_files/out_file.sigmf-data'")
            self.fileName = "./output_files/out_file.sigmf-data"
        elif(not self.fileName.endswith(".sigmf-data")):
            self.fileName += ".sigmf-data"
        
        self.sethFreq = float(item.text())
        File = open("ooga_booga.txt", "w")
        File.write(item.text()+'\n')
        File.write(self.durationLine.text()+'\n')
        File.write(self.rateLine.text()+"\n")
        File.write(self.fileName)
        File.close()
        exit(5)
        #os.system("python3 ./signal_recorder.py --center-freq "+ item.text())

    def setFilePath(self):
        self.fileName = Qt.QFileDialog.getSaveFileName(self, 'Save File', "","SigMF Data File(*.sigmf-data)")[0]

    def saveList(self):
        self.listName = Qt.QFileDialog.getSaveFileName(self, 'Save File')
        File = open(self.listName[0], "w")
        freqs = [self.freqList.item(i).text() for i in range(self.freqList.count())]
        for freq in freqs:
            File.write(str(freq)+'\n')
        File.close()

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.epy_block_1.sample_rate = self.samp_rate
        self.epy_block_1.start_frequency = self.center_freq - (self.samp_rate/2)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)

    def get_peak_threshold(self):
        return self.peak_threshold

    def set_peak_threshold(self, peak_threshold):
        self.peak_threshold = peak_threshold
        Qt.QMetaObject.invokeMethod(self._peak_threshold_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.peak_threshold)))
        self.blocks_peak_detector2_fb_0.set_threshold_factor_rise(self.peak_threshold)

    def get_peak_size(self):
        return self.peak_size

    def set_peak_size(self, peak_size):
        self.peak_size = peak_size
        self.blocks_peak_detector2_fb_0.set_look_ahead(self.peak_size)

    def get_peak_scale(self):
        return self.peak_scale

    def set_peak_scale(self, peak_scale):
        self.peak_scale = peak_scale
        Qt.QMetaObject.invokeMethod(self._peak_scale_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.peak_scale)))
        self.blocks_moving_average_xx_0.set_length_and_scale(self.avg_window_size, self.peak_scale/self.avg_window_size)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.epy_block_0.vector_size = self.fft_size
        self.epy_block_1.vector_size = self.fft_size
        self.qtgui_vector_sink_f_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        Qt.QMetaObject.invokeMethod(self._center_freq_line_edit, "setText", Qt.Q_ARG("QString", str(self.center_freq)))
        self.epy_block_1.start_frequency = self.center_freq - (self.samp_rate/2)
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)
        self.qtgui_vector_sink_f_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)
        self.qtgui_vector_sink_f_0_0.set_x_axis(self.center_freq - (self.samp_rate/2), self.samp_rate/self.fft_size)

    def get_avg_window_size(self):
        return self.avg_window_size

    def set_avg_window_size(self, avg_window_size):
        self.avg_window_size = avg_window_size
        self.blocks_moving_average_xx_0.set_length_and_scale(self.avg_window_size, self.peak_scale/self.avg_window_size)

    def refresh_freq_list(self):
        self.freqList.clear()
        self.freqList.addItems(self.epy_block_1.getFreqs())

    def configFile(self):
        if (os.path.isfile("ooga_booga.txt")):
            File = open("ooga_booga.txt", "r")
            next(File)
            self.durationLine.setText(File.readline().strip())
            self.rateLine.setText(File.readline().strip())
            self.fileName = File.readline().strip()

def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.configFile()

    tb.start()
    tb.show()

    listTimer = Qt.QTimer()
    listTimer.timeout.connect(tb.refresh_freq_list)
    listTimer.setInterval(tb.freqListRate)
    listTimer.start()
    # on a timer
    # tb.refresh_freq_list()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
