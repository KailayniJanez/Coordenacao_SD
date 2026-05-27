# Distributed Leader Election System with Docker

This project implements a distributed coordination system using leader election and fault tolerance mechanisms. The application simulates four distributed nodes running in Docker containers and communicating through TCP sockets.

## Features

- Leader election using the Bully Algorithm
- Heartbeat mechanism for failure detection
- Adaptive timeout using RTT estimation (EWMA)
- Simulated clock drift between nodes
- Automatic leader reelection after failures
- Communication through TCP sockets
- Docker-based distributed environment
- Logging system for node activity

---

## Project Structure

```text
Coordenacao_SD/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── node.py
├── election.py
├── heartbeat.py
├── adaptive_timeout.py
├── logger.py
└── logs/
```

## Technologies

- Python 3.11
- Docker
- Docker Compose
- TCP Sockets
- Multithreading

---

## System Architecture

The system consists of four nodes:

- Node 1
- Node 2
- Node 3
- Node 4

Initially, the node with the highest ID becomes the leader.

Current rule:

```text
Highest ID → Leader
```

The leader periodically sends heartbeat messages to all other nodes.

Followers monitor these heartbeats. If they stop receiving them, they detect a failure and initiate a new election process.

---

## Leader Election

The implementation uses the Bully Algorithm.

Election steps:

1. A node detects leader failure
2. It sends election messages to nodes with higher IDs
3. If a higher node responds, it waits
4. If no response is received:
   - the node becomes the leader
5. The new leader starts sending heartbeats

---

## Adaptive Timeout

Fixed timeout values were avoided.

The system dynamically adjusts timeout values using an Exponential Weighted Moving Average (EWMA):

timeout = RTT × factor

This reduces false failure detections caused by network delays.

---

## Clock Drift Simulation

To simulate non-synchronized distributed systems, each node has an artificial clock drift:

```python
clock_drift=random.uniform(-0.12,0.12)
```

This creates independent local clocks.

---

## Running the Project

Build and start containers:

```bash
docker compose up --build
```

---

## Testing Leader Failure

Stop the leader container:

```bash
docker stop node4
```

Expected behavior:

```text
Leader failed
Starting election
Node 3 became new leader
heartbeat leader=3
```

---

## Logs

Node activity is recorded in:

```text
logs/
```

Example:

```text
node1.log
node2.log
node3.log
node4.log
```

---

## Authors

Group J

- Kailayni Rodrigues Janez
- Samuel Gerga Martins
- Matheus Minasse
- Lucas Vasconcelos Fuji
- Ivan Mateus Azevedo Martinotto
  
Developed for the Distributed Systems course project.
