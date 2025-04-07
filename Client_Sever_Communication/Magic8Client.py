from socket import *

serverName = '127.0.0.1'  # Localhost IP address
serverPort = 12000  # Server port number

try:
    # Create a TCP/IP socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # Connect to the server using the specified address and port
    clientSocket.connect((serverName, serverPort))

    # Loop to continuously send/receive messages until the user decides to quit
    while True:
        # Prompt user for input; the message will be sent to the server
        sentence = input('Type a question and press Enter to get an answer (or type "bye" to quit):  ')

        # Send the input message to the server after encoding it to bytes
        clientSocket.send(sentence.encode())

        # Check if the user wants to terminate the connection
        if sentence.lower() == "bye":
            print("Closing connection...")
            break

        # Receive the server's response 
        responses = clientSocket.recv(1024)
        print('From Server:', responses.decode())  # Decode and print the server's response

# Handle the case where the server is not running or refuses the connection
except ConnectionRefusedError:
    print(f"Could not connect to server at {serverName}:{serverPort}")

# General exception handler for any other errors
except Exception as e:
    print(f"Error: {e}")

# Ensure the socket is closed when exiting, even if an error occurs
finally:
    clientSocket.close()
    print("Client socket closed.")
