# CoAP_Parking
## Consists of CoAP server which uses Client/Server architecture.

The CoAP server stores the map for parking lot and has the information of all the empty and occupied parking positions in the parking area. 
Parking Model consists of sensor attached to every parking slot. These sensors run udp client to send their status to the server.
Also every new car arriving runs a udp client and makes a request to CoAP server to get and reserve a empty parking slot. All the connections and request goes over UDP using CoAP Protocol. 
Multiple client tries to connect to broker in separate threads to the server. The service time of each client is noted to study the queuing delay and waiting time for customers to get their request served.
Traffic coming to the server follows the poisson arrival.

## Code Changes:-
### Server side handling:-
Created a new server test_server.c to store the parking positions map and handle incoming client requests.

File Location:- libcoap-code/examples/

### Client side changes:- 
A python script is run to send multiple requests.
The system runs of 3 types of clients corresponding to 3 request types.
* Put Client: Request from sensor placed at parking positon to occupy the position in map.
* Delete Client: Request from sensor placed at parking position to empty it and add in pool of free slots.
* Get Client: New customer arriving at the server asking to reserve and return a free slot.

Client threads are running independent of each other and service time for each client is noted to evaluate prformance. Clients are arriving according to Poisson Distribution.

File Location:- libcoap-code/examples/parking_simulation.py

## Installation:-
* Inside libcoap-code folder run sudo make install
* Type following commands to run CoAP Server - cd examples/ and ./test-server
* Now to run parking simulation open a new tab in current directory and run python parking_simulation.py

## Simulation Details:-
The simulation runs three separate threads for three types of clients. Thus simultaneously pushing out several requests on the single server. The service time is then noted for each clients and written in csv files "get_simulation_service_time.csv", "put_simulation_service_time.csv", "delete_simulation_service_time.csv". Also the mean service time and server throughput is written in corresponding results.csv files. Graphs are plotted to analyse the queueing delay on changing the mean arrival rates of these client requests and also the server utilization.
