# The implementation of a congestion control mechanism. Demonstrative application (UDP)

The congestion of a network is a state that appears when the trafic is heavy that it slows down the response time of the network. With other words, in the network there is more data than it should be. The side effects are: late, packets loss or blocking of new connections. The congestion control is a mechanism to prevent these problems.

## UDP Protocol

UDP (User Datagram Protocol) is a protocol that sends independent packets of data, called datagrams, from one computer to another, without guaranteeing in any way that they reach their destination. <br/><br/>
It is a non-connection oriented service: no connection is established between the client and the server. So the server does not wait for connection calls, but directly receives datagrams from clients. <br/><br/>
It is found in client-server systems where few messages are passed and generally too infrequently to maintain an active connection between the two entities. <br/><br/>
Order of message receipt and prevention of packet loss are not guaranteed. UDP is mostly used in networks where there is very little packet loss and in applications where packet loss is not very serious (e.g. video streaming applications). <br/>

## Congestion control


The UDP protocol is packet-oriented and not connection-oriented, as is the case with the TCP protocol.<br/></br>
Within the TCP protocol, there are a number of algorithms that deal with the occurrence of congestion. Among them, we mention: Tahoe, Reno, New Reno and Vegas.<br></br>
The application will implement the functionality of the _Tahoe_ algorithm for transmitting packets using UDP in a **client-server** architecture.

## Tahoe algorithm

The Tahoe algorithm was named after a lake in the United States of America. This particular algorithm was developed in that area, hence the name.<br/><br/>
The algorithm states are: **Slow Start**, **AIMD** and **Fast Retransmit**.<br/><br/>
**Slow Start state**: The state is active until the window size (_cwnd_) becomes equal to _sshtresh_.
In this phase, the window size doubles at each data segment sent and received (_RTT_).
When cwnd reaches the value of sshtresh, the state ceases and gives way to the **AIMD** state.<br/>

**AIMD Status**: In this phase _cwnd_ increases according to the formula **CWND = MSS * MSS / CWND**, where _MSS_ is the maximum size of a segment.
At the same time, _sshtresh_ will be reduced to half the current value of _cwnd_.<br/>

**Fast Retransmit state**: When three duplicate packets are received as a response, the algorithm enters this phase.
Here _cwnd_ value is set to 1, then packet transmission will resume in **Slow Start** state.

## Server configuration

Configuring a server is done by specifying the IP address and source port. They must also be known by the client who wants to connect.

## Establishing the connection to the server

1. The connection is made by specifying the IP address, the source port (client) and the destination port (server).
2. After establishing the communication parameters, the connection to the database and the validation of the user who wants to use the interface will be carried out.
3. Then the interface becomes active and the user can send and receive packets from the server.

## The format of the packets to be sent

To begin with, any packet will consist of 8 bits in which the desired control type will be stored.

| Control type | Code |
|--------------|------|
| CONNECTION   | 0    |
| INSTRUCTION  | 1    |
| RESPONSE     | 2    |

On the following 8 bits, the type of command that is to be executed, within the INSTRUCTION type package or that was executed, within the RESPONSE type package, will be saved.

| Command name | Code |
|--------------|------|
| LIST_FILES   | 0    |
| CREATE_FILE  | 1    |
| APPEND_FILE  | 2    |
| REMOVE_FILE  | 3    |

If the packet is of type CONNECTION, the byte will contain the following types of notifications:

| Notification type | Code |
|-------------------|------|
| ACK               | 0    |
| LEAVE             | 1    |
| OVER              | 2    |

## The structure of the packets through which the communication will be carried out

For the packet that will request __show files__, __complete transmission__ or __disconnect from server__, the structure is:

| INSTRUCTION_CODE | COMMAND_CODE |
|------------------|--------------|
| 8 BITS           | 8 BITS       |

For the package that will ask to __add a file__ or __delete a file__, the structure is:

| INSTRUCTION_CODE | COMMAND_CODE | FILENAME |
|------------------|--------------|----------|
| 8 BITS           | 8 BITS       | x BITS   |


For the package that will perform __add content__, __download a file__ or __upload a file__, the structure is:

| INSTRUCTION_CODE | COMMAND_CODE | CURRENT_PACKET_NUMBER | PACKET_NUMBERS | FILENAME | PACKET_CONTENT |
|------------------|--------------|-----------------------|----------------|----------|----------------|
| 8 BIȚI           | 8 BIȚI       | 8 BIȚI                | 8 BIȚI         | x BIȚI   | 1 - 512 BIȚI   |

For the package that will perform __data confirmation__, the structure is:

| INSTRUCTION_CODE | COMMAND_CODE | NEXT_PACKET_NUMBER |
|------------------|--------------|--------------------|
| 8 BIȚI           | 8 BIȚI       | 8 BIȚI             |

## Operations implemented

Using the package structure defined above, the application will implement the following operations:
- creating a file
- adding content to a file
- deleting a file

We remind you that the congestion control mechanism using the Tahoe Algorithm will be realized only in the case of the second operation, in which the content to be added will be divided into packets that will be sent to the server.

## Programming paradigms used

In implementing the application, the paradigm of object-oriented programming was used, but also elements of functional programming.<br/>

The application uses several design templates:
- Builder (Builder) - for creating packages;
- Factory of objects (Factory) - for formatting packages according to the operation performed;
- Command (Commander) - for performing server response operations after receiving a packet;
- Finite State Machine - for congestion management, used by Client and Server.

The UML class diagram is as follows:

![UML Diagram](UML_Diagram.png)

## Results

Below are the results obtained from the transfer of 176 datagrams, which carried the contents of a text file,
during which the server had a 95% packet delivery rate.

![CWND Evolution Plot](Statistics/grafic.png)

## Bibliography

[1] TCP/IP Illustrated, Volume 2, W. Richard Stevens and Gary R. Wright, Addison-Wesley Professional<br/>

[2] RFC 768, User Datagram Protocol, J. Postel, 28 August 1980<br/>

[3] RFC 2914, Congestion Control Principles, S. Floyd, September 2000<br/>

[4] RFC 5681, TCP Congestion Control, Purdue University, September 2009<br/>