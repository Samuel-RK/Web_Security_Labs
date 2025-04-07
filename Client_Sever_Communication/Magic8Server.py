from socket import *
import random

serverPort = 12000
serverName = '127.0.0.1'

# List of responses that the server will randomly send to the client
responses = ['Signs point to yes',
             'Without a doubt',
             'You may rely on it',
             'Do not count on it',
             'Looking good',
             'Cannot predict now',
             'It is decidedly so',
             'Outlook not so good']

# Function to select a random response from the list and return it
def respond_to_question():
    return random.choice(responses)

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

            # Loop to maintain communication with the connected client
            while True:
                # Receive a message from the client and decode it
                sentence = connectionSocket.recv(1024).decode()

                # End the connection if the client sends "bye"
                if sentence.lower() == "bye":
                    print(f"Shutting down connection by request from {addr}")
                    connectionSocket.send("Server is shutting down...".encode())
                    serverSocket.close()  # Close the server socket, stopping new connections
                    break  # Exit the inner loop, ending communication with the client

                # Sends a random response to the client
                response = respond_to_question()
                connectionSocket.send(response.encode())

        except OSError:  # Handle errors like invalid file descriptors or socket issues
            print("Server socket closed, no more clients will be accepted.")
            break  # Exit the outer loop, ending the server process

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