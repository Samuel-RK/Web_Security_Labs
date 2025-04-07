from socket import *
import os
from datetime import datetime

# Server configuration
serverPort = 56789
serverName = '127.0.0.1'

try:
    # Create a TCP socket using IPv4 and bind it to the specified address and port
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((serverName, serverPort))
    serverSocket.listen(1)  # Listen for incoming connections (1 client at a time)
    print('The server is ready to receive')

    # Infinite loop to continuously accept and handle new client connections
    while True:
        try:
            # Accept a new connection from a client
            connectionSocket, addr = serverSocket.accept()
            request = connectionSocket.recv(1024).decode()
            request_lines = request.split('\r\n')

            if len(request_lines) > 0:
                # Parse the request line (method, file name, HTTP version)
                first_line = request_lines[0]
                split_request = first_line.split()
                if len(split_request) > 0:
                    request_method = split_request[0]
                    file_name = split_request[1]
                    http_version = split_request[2]

                    # Only handle GET requests, return 405 for other methods
                    if request_method != 'GET':
                        status_line = 'HTTP/1.1 405 Method Not Allowed\r\n'
                        headers = 'Allow: GET\r\n\r\n'
                        connectionSocket.send((status_line + headers).encode())
                    else:
                        # Remove the leading slash from the file name and add .html if no extension is provided
                        file_name = file_name.lstrip('/')
                        if not os.path.splitext(file_name)[1]:
                            file_name += '.html'

                        # Check if the file exists
                        if os.path.exists(file_name):
                            # Read the file content
                            with open(file_name, 'rb') as f:
                                content = f.read()

                            # Determine content type (HTML in this case)
                            content_type = 'text/html'

                            # Construct the HTTP response
                            status_line = 'HTTP/1.1 200 OK\r\n'
                            headers = f'Server: cyberpro\r\n'
                            headers += f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\n'
                            headers += 'Content-Language: en\r\n'
                            headers += f'Content-Type: {content_type}\r\n'
                            headers += f'Content-Length: {len(content)}\r\n'
                            headers += '\r\n'  # Blank line between headers and content

                            # Send the response
                            connectionSocket.send(status_line.encode())
                            connectionSocket.send(headers.encode())
                            connectionSocket.send(content)
                        else:
                            # File not found, return 404 response
                            status_line = 'HTTP/1.1 404 Not Found\r\n'
                            headers = f'Server: cyberpro\r\n'
                            headers += f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}\r\n'
                            headers += 'Content-Language: en\r\n'
                            headers += 'Content-Type: text/html\r\n'
                            headers += '\r\n'
                            body = '<html><body><h1>404 Not Found</h1></body></html>'

                            # Send 404 response
                            connectionSocket.send(status_line.encode())
                            connectionSocket.send(headers.encode())
                            connectionSocket.send(body.encode())

        except OSError:
            print("Server socket closed, no more clients will be accepted.")
            break
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            connectionSocket.close()

except KeyboardInterrupt:
    print("\nServer shutting down...")
except Exception as e:
    print(f"Error: {e}")
finally:
    serverSocket.close()
    print("Server connection closed.")
