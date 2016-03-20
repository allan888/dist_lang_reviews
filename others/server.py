#!/usr/bin/env python
# -*- coding: utf-8 -*-

def tcplink(sock, addr):
    sock.send('Welcome...')
    while True:
        data = sock.recv(1024)
        if data == 'exit' or not data:
            break
        print "receive:",data
        sock.send('Hello, %s' % (data))
    sock.close()

if __name__ == '__main__':
    import socket, threading, os
    from multiprocessing import Process
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 1024))
    s.listen(5)
    while True:
        sock, addr = s.accept()
        # t = threading.Thread(target=tcplink, args=(sock, addr))
        # t.start()
        p = Process(target=tcplink, args=(sock,addr))
        p.start()
