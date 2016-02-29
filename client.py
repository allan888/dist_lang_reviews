#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 1024))
    print s.recv(1024)
    for data in ['1', '2', '3']:
        s.send(data)
        print s.recv(1024)
    s.send('exit')
    s.close()
