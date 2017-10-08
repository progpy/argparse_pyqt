#!/usr/bin/python3

import socket
import select


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 12345))
    sock.listen(socket.SOMAXCONN)

    connections = [sock]
    while True:
        r_read, r_write, r_error = select.select(connections, [], [], 1)
        for s in r_read:
            if s == sock:
                client, addr = sock.accept()
                connections.append(client)
                print("New client: {}:{}".format(*addr))
                continue

            data = s.recv(100)
            if data == b'':
                print("{}:{} disconnected".format(*s.getpeername()))
                connections.remove(s)
                continue

            _from = "{}: ".format(s.getpeername()[0])
            for c in connections:
                if c not in [s, sock]:
                    try:
                        c.sendall(_from.encode())
                        c.sendall(data)
                    except Exception as e:
                        pass

if __name__ == '__main__':
    main()
