#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Bertrand256
# Created on: 2017-03

import os
import sys

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from ui import ui_about_dlg
from wnd_utils import WndUtils


class AboutDlg(QDialog, ui_about_dlg.Ui_AboutDlg, WndUtils):
    def __init__(self, parent, app_version_str):
        QDialog.__init__(self, parent)
        ui_about_dlg.Ui_AboutDlg.__init__(self)
        WndUtils.__init__(self, parent.config)
        self.app_version_str = app_version_str
        self.setupUi()

    def setupUi(self):
        ui_about_dlg.Ui_AboutDlg.setupUi(self, self)
        self.setWindowTitle("About")
        img = QPixmap(os.path.join(self.app_config.app_path, "img/masternode-tool.png"))
        img = img.scaled(QSize(64, 64))
        self.lblImage.setPixmap(img)
        self.lblAppName.setText('Masternode Tool ' + self.app_version_str)
        self.textAbout.setOpenExternalLinks(True)
        self.textAbout.viewport().setAutoFillBackground(False)
        if sys.platform == 'win32':
            # self.resize(600, 390)
            self.textAbout.setHtml(self.textAbout.toHtml().replace('font-size:11pt', 'font-size:8pt'))
            # self.textAbout.setHtml(self.textAbout.toHtml().replace('font-size:9pt', 'font-size:8pt'))
        elif sys.platform == 'darwin':
            self.textAbout.setHtml(self.textAbout.toHtml().replace('font-size:11pt', 'font-size:14pt'))
        # elif sys.platform == 'linux':
        #     self.resize(620, 400)
        # self.layout().setSizeConstraint(QLayout.SetFixedSize)

    @pyqtSlot(bool)
    def on_btnClose_clicked(self):
        self.close()
