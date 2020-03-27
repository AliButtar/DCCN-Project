# DCCN-Project

COMPUTER COMMUNICATION AND NETWORKING
SEMESTER PROJECT
# MULTI THREADED SERVER AND CLIENTS WITH JEOPARDY PROTOCOL IMPLEMENTATION
Muhammad Ali Buttar
FA17-BSE-075


## Abstract
This project is about implementation about a multi-threaded server and client. A server can accept more
than one client. Server and Clients interact with each other to play Jeopardy game of questions and answers
and client’s respective scores are updated


## Introduction
We developed a multi-threaded client/server application. The server we developed can handle
more than one connection at a time. The main goal is to implement jeopardy game, where more
than one client can connect to server and able to play the game.
There are two categories. When two or more than two clients are connected to the server then
server chooses randomly one client and allow that client to choose one of the two categories.
When category is selected than server throws first question from the quiz from chosen category.
One of the clients has to ring the buzzer and then have to answer the question. If answer is correct
or answer is wrong the respected client’s score is updated. After updating score, the first round
will come to an end and then server starts second round.
After completing all rounds from all categories, the server will finish the game and notifies the
clients who is the winner.
Design Details



## Threading

### Server Side
A pool of single thread is created which allotted to only accepting any incoming connections at
any time after the socket has been created and binded. For every connection accepted there is a
specific class for threading and clients in which every connection from a client creates a new
connection and two threads are created and started for each client. One thread manages sending
the messages to the client while the second thread manages receiving messages from the client.
The connection object for each client is passed into the method which receives the messages so
that each client can send messages on their own separate connection.
There are methods created for sending and receiving messages. Each of them contains the
necessary functionality which deals with how messages from the Clients are interpreted and also
how the messages sent from the client will notify the clients about starting the new round, notifying
the connected clients that they are in the game etc.4
Methods/ Classes in Server
1. ClientThread Class
This class is responsible for initiating the connection object. The class basically accepts port
number, IP of client.
The next method ‘run’ basically assign task to thread. The thread is sending messages from server
as well as receive messages from clients.5
2. Create Socket Method
As the names of both methods define that these methods are creating and binding socket
respectively.6
3. Accept Connection Method
The method basically accepts the connections from clients respectively.


### Client Side
Each client contains a pool of two threads as well which are used similar to how they are used in
the server, each one is used for sending and receiving messages. After the necessary methods of
creating, binding the socket, the request for connection is sent to the server. Each of the method
for two threads is called upon to start the process of communicating with the server. All the
Questioning, score etc. are handled by the server7
1. Send Message Method
This method is responsible for sending massage to server.
2. Receiving message method
This method is responsible for receiving massage from server.
Jeopardy Functionality
The two methods in Server called “Send_Message()” and “Receiveing_Message(conn)” handle all
of the functionality of the jeopardy game functionality. The send message starts the new round and
notifies the clients that are in the game and then randomly one of them is presented with the option
to choose the category. The answer by the client is taken as input in the receiving message method
and then all the clients are presented with the question. Whoever types ‘ring’ first will be able to
answer the question. Again, the answer will be checked on server side if it is correct or wrong and
then the new round will be started by the server.
