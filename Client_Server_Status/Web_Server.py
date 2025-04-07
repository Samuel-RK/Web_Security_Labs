from socket import *
import os
from datetime import datetime

serverPort = 56789
serverName = '127.0.0.1'

try:
    # Create a TCP socket using IPv4 and bind it to the specified address and port
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to the server's IP address and port, allowing it to receive incoming connections
    serverSocket.bind((serverName, serverPort))

    # Listen for incoming connections; allow up to 1 connection
    serverSocket.listen(1)
    print('The server is ready to receive')

    # Infinite loop to continuously accept and handle new client connections
    while True:
        try:
            # Accept a new connection from a client; blocks until a client connects
            connectionSocket, addr = serverSocket.accept()  # Establishes the connection (TCP 3-way handshake)
            request = connectionSocket.recv(1024).decode()
            request_lines = request.split('\r\n')

            if len(request_lines) > 0:
                first_item = request_lines[0]
                split_get = first_item.split()
                if len(split_get) > 0:
                    request_method = split_get[0]
                    file_name = split_get[1]
                    http_version = split_get[2]
                    file_name = file_name.lstrip('/')

                    # Only Handle GET requests and return 405 for other methods
                    if request_method == 'GET':

                        if not os.path.splitext(file_name)[1]:
                            file_name += '.html'
                            # print('The name', file_name)

                        if os.path.exists(file_name):

                            with open(file_name, 'rb') as f:
                                content = f.read()

                            # Determine content type
                            if file_name.endswith('.html'):
                                content_type = 'text/html'

                            # Construct HTTP response
                            status_line = 'HTTP/1.1 200 OK\r\n'
                            headers = ''
                            headers += 'Server: cyberpro\r\n'
                            headers += f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\n'
                            headers += 'Content-Language: en\r\n'
                            headers += f'Content-Type: {content_type}\r\n'
                            headers += f'Content-Length: {len(content)}\r\n'
                            headers += '\r\n'  # Blank line between headers and content
                            # Send response
                            response = status_line + headers

                            connectionSocket.send(response.encode())
                            connectionSocket.send(content)

                        else:
                            # File Not Found, return 404 response
                            status_line ='HTTP/1.1 404 Not Found\r\n'
                            headers = ''
                            headers += 'Server: cyberpro\r\n'
                            headers += f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\n'
                            headers += 'Content-Language: en\r\n'
                            headers += 'Content-Type: text/html\r\n'
                            body = '<html><body><h1>404 Not Found </h1></body></html>'
                            headers += f'Content-Length: {len(body)}\r\n'
                            headers += '\r\n'

                            # Send 404 response
                            response = status_line +headers+ body
                            connectionSocket.send(response.encode())


        except Exception as e:  # General exception handler for any other errors during client handling
            print(f"Error handling client {addr}: {e}")

        finally:
            # Close the connection with the client after the interaction ends (finishes the TCP 3-way handshake)
            connectionSocket.close()

except KeyboardInterrupt:
    # Handle server shutdown via keyboard interrupt
    print("\nServer shutting down...")
except Exception as e:
    # Handle any other errors during the server setup or operation
    print(f"Error: {e}")
finally:
    # Ensure the server socket is closed when the server shuts down
    serverSocket.close()
    print("Server connection closed.")