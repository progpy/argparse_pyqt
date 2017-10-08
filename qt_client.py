#!/usr/bin/env python3

import sys
from PyQt5 import QtNetwork, QtWidgets, QtCore


class ConnectionWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ConnectionWindow, self).__init__(parent, flags=QtCore.Qt.Dialog)

        self.ip = QtWidgets.QLineEdit('127.0.0.1')
        self.port = QtWidgets.QLineEdit('12345')
        self._buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        layout2 = QtWidgets.QGridLayout()
        layout2.setSpacing(5)
        layout2.addWidget(QtWidgets.QLabel('Server IP: '), 0, 0)
        layout2.addWidget(self.ip, 0, 1)
        layout2.addWidget(QtWidgets.QLabel('Port: '), 1, 0)
        layout2.addWidget(self.port, 1, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.addLayout(layout2)
        layout.addWidget(self._buttons, alignment=QtCore.Qt.AlignHCenter)  # AlignLeft

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self.setLayout(layout)


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ChatWindow, self).__init__(parent, flags=QtCore.Qt.Window)

        self._sock = QtNetwork.QTcpSocket()
        self._sock.connected.connect(self._connected)
        self._sock.readyRead.connect(self._read)
        self._sock.disconnected.connect(self._disconnected)

        self.statusBar().showMessage('Waiting for params...')

        self._conn_dialog = ConnectionWindow(parent=self)
        self._conn_dialog.setModal(True)
        self._conn_dialog.accepted.connect(self._connect)
        self._conn_dialog.rejected.connect(self.close)

        self._input = QtWidgets.QLineEdit()
        self._send_button = QtWidgets.QPushButton('&Send')
        self._send_button.setDisabled(True)
        self._input.returnPressed.connect(self._send_button.click)
        self._send_button.clicked.connect(self._send)

        self._messages = QtWidgets.QTextEdit()
        self._messages.setReadOnly(True)

        main_widget_layout = QtWidgets.QGridLayout()
        main_widget_layout.setSpacing(5)
        main_widget_layout.addWidget(self._messages, 1, 0, 1, 2)
        main_widget_layout.addWidget(self._input, 2, 0)
        main_widget_layout.addWidget(self._send_button, 2, 1)

        main_widget = QtWidgets.QWidget(flags=QtCore.Qt.Widget)
        main_widget.setLayout(main_widget_layout)

        self.setCentralWidget(main_widget)
        self.resize(400, 300)
        self.setWindowTitle('Chat')

    def _connected(self):
        self.statusBar().showMessage('Connected!')
        self._send_button.setEnabled(True)

    def _connect(self):
        try:
            self._ip = self._conn_dialog.ip.text()
            self._port = int(self._conn_dialog.port.text())
        except Exception:
            self.statusBar().showMessage('connection error')
            return

        self.statusBar().showMessage('Connecting to {}:{}...'.format(
            self._ip, self._port))

        self._sock.connectToHost(self._ip, self._port)

    def _disconnected(self):
        self.statusBar().showMessage('Disconnected')
        self._send_button.setDisabled(True)

    def _read(self):
        while self._sock.bytesAvailable():
            message = self._sock.readAll().data().decode()
            self._messages.append(message)

    def _send(self):
        _text = self._input.text()
        if not _text:
            return

        self._input.setText('')
        self._sock.write(_text.encode())
        self._messages.append('Me: {}'.format(_text))

    def get_params(self):
        self._conn_dialog.show()


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = ChatWindow()
    window.get_params()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
