#!/usr/bin/env python
import logging
import select
import socket
from multiprocessing import Process


def start_udp_client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = '0.0.0.0'
    server_port = port

    server = (server_address, server_port)
    sock.bind(server)
    print("Listening on " + server_address + ":" + str(server_port))
    while True:
        data, client_address = sock.recvfrom(65535)
        if data:
            response = data
            print(response)
            sent = sock.sendto(response, client_address)


def start_udp_client_helper():
    start_udp_client(33333)


def start_tcp_client(port):
    ip = "localhost"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f'Binding to {ip}:{port}')
    server.bind((ip, port))
    server.setblocking(False)
    server.listen(100)
    logging.info(f'Listening on {ip}:{port}')

    readers = [server]

    while True:
        readable, writable, errored = select.select(readers, [], [], 0.5)

        for s in readable:
            try:
                if s == server:
                    client, address = s.accept()
                    client.setblocking(False)
                    readers.append(client)
                    logging.info(f'Connection: {address}')
                else:
                    data = s.recv(1024)
                    if data:
                        logging.info(f'Echo: {data}')
                        s.send(data)
                    else:
                        logging.info(f'Remove: {s}')
                        s.close()
                        readers.remove(s)

            except Exception as ex:
                logging.warning(ex.args)
            finally:
                pass


def start_tcp_client_helper():
    start_tcp_client(33332)


if __name__ == '__main__':
    start_tcp_client_helper()
    # p1 = Process(target=start_udp_client_helper)
    # p1.start()
    # p2 = Process(target=start_tcp_client_helper)
    # p2.start()
    # p1.join()
    # p2.join()
