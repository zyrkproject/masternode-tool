#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import PyQt5.QtWidgets as qwi
from PyQt5.QtGui import QIcon
import main_dlg
import traceback
import logging

from wnd_utils import WndUtils

if __name__ == '__main__':
    def my_excepthook(type, value, tback):
        print('=========================')
        traceback.print_tb(tback)
        for fh in logging.RootLogger.root.handlers:
            if isinstance(fh, logging.FileHandler):
                traceback.print_exception(type, value, tback, file=fh.stream)
                fh.flush()
        WndUtils.errorMsg(str(value))

    sys.excepthook = my_excepthook

    if getattr(sys, 'frozen', False):
        app_path = base_path = sys._MEIPASS
        os.environ['SSL_CERT_FILE'] = os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    else:
        app_path = os.path.dirname(__file__)
        path, tail = os.path.split(app_path)
        if tail == 'src':
            app_path = path

    app = qwi.QApplication(sys.argv)
    ui = main_dlg.MainWindow(app_path)
    ui.show()

    try:
        ico_path = os.path.join(app_path, 'img', 'masternode-tool.ico')
        if os.path.exists(ico_path):
            app_icon = QIcon(ico_path)
            app.setWindowIcon(app_icon)
    except:
        pass

    sys.exit(app.exec_())

