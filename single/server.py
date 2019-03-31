import socket
import sys


#Creating a socket
def create_socket():
    try:
        global host
        global port
        global s
        host=""
        port=9999
        s=socket.socket()

    except socket.error as msg:
        print("Socket creation error: ",+str(msg))


#Binding the socket and listenting for connection
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: "+str(port))
        s.bind((host,port))
        s.listen(5)
        
    except socket.error as msg:
        print("Binding error: ",+str(msg) +"\n"+"Retrying...")
        bind_socket()


#Establish connection with a client (socket must be listenting)
def socket_accept():
    conn,address=s.accept()
    print("connection has been established! |"+ "IP " +str(address[0]) +" | Port"+str(address[1]))
    send_command(conn)
    conn.close()


#Send command to client
def send_command(conn):
    while True:
        cmd=input()
        if cmd=='quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response=str(conn.recv(1024),"utf-8")
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
    
