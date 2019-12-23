import socket
import threading
from queue import Queue
from random import randrange

NUMBER_OF_THREAD = 1
JOBS = [1]
threads = []
recv_threads = []

all_conn = []
all_addr = []

queue = Queue()

conn = None

cat = ['Animals', 'Countries']

q1 = ['How many legs does cat have ?', 'how many legs does chicken have ?']
a1 = ['4', '2']
q2 = ['Whats the area of Pakistan ?', 'Name a superpower ?']
a2 = ['8', 'pak']

score1 = 0
score2 = 0
cat_id = 0
n = 0
m = 0
client = 0

class ClientThread(threading.Thread):


    def __init__(self, ip, port1, socket1, i, conn12):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port1 = port1
        self.socket1 = socket1
        self.i = i
        self.conn12 = conn12
        print("[+] New thread started for " + self.ip + ":" + str(self.port1))

    def run(self):
        # print("Connection from : " + self.ip + ":" + str(self.port1))

        if self.i == 0:
            send_message()

        if self.i == 1:
            recv_message(self.conn12)


def create_socket():
    try:
        global host
        global port
        global s

        s = socket.socket()
        host = ''
        port = 5000

        print("Socket Created")
    except socket.error as msg:
        print("error creating the socket " + str(msg))


def bind_socket():
    global host
    global port
    global s

    print("Socket binded to : " + str(port))
    s.bind((host, port))
    s.listen(5)  # number of clients that can be connected
    print("Socket is Listening")


def accept_connections():
    global host
    global port
    global s
    global conn

    for c in all_conn:
        c.close()

    del all_addr[:]
    del all_conn[:]

    while True:
        try:
            i = 0
            conn, address = s.accept()
            s.setblocking(1)

            newthread = ClientThread(host, port, s, i, conn)
            newthread.start()
            threads.append(newthread)
            i = 1
            newthread1 = ClientThread(host, port, s, i, conn)
            newthread1.start()
            recv_threads.append(newthread1)

            all_conn.append(conn)
            all_addr.append(address)

            # list_connections()
        except:
            print("error in accepting connections")


def send_message():
    while True:
        try:
            msg = input("Server Message: ")
            if msg == 'start':
                in_game()
                new_round()
                get_target()
            if msg == 'stop':

                break;
            if msg == 'list':
                list_connections()
            if msg == 'finish':
                winner()
            if len(str.encode(msg)) > 0 and msg!='start':
                for x in all_conn:
                    x.send(str.encode(msg))
        except:
            print("error sending message")
            break


def get_target():
    conn1 = None
    try:
        rand = randrange(len(all_conn))
        conn1 = all_conn[rand]
        i = 0

        conn1.send(str.encode('Press 1 for '+cat[0] + '\n' + 'Press 2 for '+cat[1] +'\n'))

        for x in all_conn:
            if x != conn1:
                x.send(str.encode('Please wait\n'))
            i += 1

    except:
        print("selection no valid")
        return None


def in_game():
    for x in all_conn:
        x.send(str.encode("You are in the game"))


def new_round():
    for x in all_conn:
        x.send(str.encode('The new Round has started !!\n '))


def send_all(message):
    for x in all_conn:
        x.send(str.encode(message))


def winner():
    global score1
    global score2

    if(score1 > score2):
        send_all('The winner of the game is client1 with score '+str(score1))
        send_all('The loser is client2 with score '+str(score2))
    else:
        send_all('The winner of the game is client2 with score ' + str(score2))
        send_all('The loser is client1 with score ' + str(score1))



def recv_message(conn1):
    global cat_id
    global n
    global m
    global client
    global score1
    global score2

    while True:
        try:
            if conn1 is not None:
                # receiving messages
                msg = str(conn1.recv(20480), 'utf-8')

                # who rang the bell
                if 'ring' in msg[2:]:
                    client = msg
                    client = client[0:1]
                    print("THIS IS " + client)
                    send_all('The buzzer has been rang by '+client)

                # check the answer conditions


                elif cat_id == 0 and msg == '1':
                    cat_id = 1
                    send_all('Category Animal has been selected')
                    send_all(q1[n])

                elif cat_id == 1 and msg == a1[n]:
                    send_all('client '+client+' has given correct answer\n')
                    cat_id = 0
                    n = n + 1

                    if client == '1':
                        score1 = score1 + 5
                    else:
                        score2 = score2 + 5
                    send_all('Client1 got ' + str(score1))
                    send_all('client2 got ' + str(score2)+'\n')
                    if (n > 1):
                        n = 0
                        send_all('Note: Catagory 1 Questions are completed. Reset to 0')

                elif cat_id == 1 and msg!= a1[n] and 'ring' not in msg:
                    send_all('client ' + client + ' has not given correct answer\n')
                    cat_id = 0
                    n = n + 1

                    send_all('Client1 got ' + str(score1) + '\n')
                    send_all('client2 got ' + str(score2) + '\n')

                    if (n > 1):
                        n = 0
                        send_all('Note: Catagory 1 Questions are completed. Reset to 0')

                elif cat_id == 0 and msg == '2':
                    cat_id = 2
                    send_all('Category Countries has been selected\n')
                    send_all(q2[m])

                elif cat_id == 2 and msg == a2[m]:
                    send_all('client '+client+' has given correct answer')
                    cat_id = 0
                    m = m + 1
                    if client == '1':
                        score1 = score1 + 5
                    else:
                        score2 = score2 + 5
                    send_all('Client1 got ' + str(score1) +'\n')
                    send_all('client2 got ' + str(score2) + '\n')

                    if (m > 1):
                        m = 0
                        send_all('Note: Catagory 2 Questions are completed. Reset to 0')

                elif cat_id == 2 and msg != a1[m] and 'ring' not in msg:
                    send_all('client ' + client + ' has not given correct answer\n')
                    cat_id = 0
                    m = m + 1
                    send_all('Client1 got ' + str(score1))
                    send_all('client2 got ' + str(score2) + '\n')
                    if (m > 1):
                        m = 0
                        send_all('Note: Catagory 2 Questions are completed. Reset to 0')





                print("Client Message: " + msg)
        except:
            print("error in receiving messages from client")
            break


def list_connections():
    print("----Clients----- \n ")
    for i, conn in enumerate(all_conn):
        try:
            conn.send(str.encode(' '))
            # conn.recv(201480)
        except:
            del all_addr[i]
            del all_addr[i]
            continue

        print(str(i) + "   " + str(all_addr[i][0]) + "    " + str(all_addr[i][1]))


def create_workers():
    for _ in range(NUMBER_OF_THREAD):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()

        if x == 1:
            create_socket()
            bind_socket()
            accept_connections()

            for t in threads:
                t.join()
            for th in recv_threads:
                th.join()

        queue.task_done()


def create_jobs():
    for x in JOBS:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()
