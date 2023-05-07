import socket
import os

# membuat socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# mengaitkan socket ke alamat dan port tertentu
server_address = ('localhost', 8080)
server_socket.bind(server_address)

# mendengarkan koneksi masuk
server_socket.listen(1)
print('Server is listening on port 8080...')

while True:
    # menerima koneksi masuk
    client_socket, client_address = server_socket.accept()
    print(f'Connection from {client_address} has been established!')

    # menerima data dari client
    data = client_socket.recv(1024).decode('utf-8')
    print(f'Received data from client: {data}')

    # memparsing HTTP request
    request_method = data.split(' ')[0]
    request_file = data.split(' ')[1]

    # mencari file yang diminta oleh client
    file_path = os.getcwd() + request_file
    if os.path.isfile(file_path):
        # membuka file dan membacanya
        with open(file_path, 'rb') as file:
            file_content = file.read()
        # membuat HTTP response message
        response = 'HTTP/1.1 200 OK\n\n' + file_content.decode('utf-8')
    elif request_file == "/500":
        # membuat HTTP response message untuk error 500
        response = 'HTTP/1.1 500 Internal Server Error\n\nError: Server Error'
    elif request_file == "/300":
        # membuat HTTP response message untuk error 300
        response = 'HTTP/1.1 300 Multiple Choices\n\nError: Multiple Choices'
    else:
        # jika file tidak ditemukan, mengirimkan pesan "404 Not Found"
        response = 'HTTP/1.1 404 Not Found\n\nFile Not Found'

    # mengirimkan response message ke client
    client_socket.sendall(response.encode('utf-8'))

    # menutup koneksi dengan client
    client_socket.close()
