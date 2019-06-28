import socket
while 1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 31001))
        client_socket.sendall(';\n')
        client_socket.recv(4)
