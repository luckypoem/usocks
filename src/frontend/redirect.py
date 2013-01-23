# coding: UTF-8

import errno
import socket

class FrontendServer(object):

    server = "localhost"
    port = 80

    def __init__(self, **opts):
        if 'server' in opts:
            self.server = opts['server']
        if 'port' in opts:
            self.port = opts['port']
        
        # initialize socket
        self.conn = socket.socket()
        self.conn.connect((self.server, self.port))
        self.conn.setblocking(0)
        self.send_buf = b""

    def send(self, data=None):
        if data:
            self.send_buf += data
        return self._continue()

    def _continue(self):
        if self.send_buf:
            try:
                sent = self.conn.send(self.send_buf)
            except socket.error as e:
                if e.errno == errno.EWOULDBLOCK:
                    sent = 0
                else:
                    raise
            if sent:
                self.send_buf = self.send_buf[sent:]
        return not self.send_buf

    def recv(self):
        data = self.conn.recv(4096)
        if data == b"":
            data = None
        return data

    def close(self):
        self.conn.close()

    def fileno(self):
        return self.conn.fileno()