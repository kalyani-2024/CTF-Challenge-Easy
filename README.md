# Quantum Relay Network (CTF Challenge)

A Flask-based CTF challenge that simulates a quantum communication network. Participants must navigate through a sequence of interactions between three nodes (Alice, Bob, and Charlie) to retrieve the hidden flag.

## Challenge Description

This challenge simulates a Quantum Relay Network where entanglement must be established and swapped between nodes to teleport information. 
The flag is split into three parts, each held by one of the agents:
1. **Alice**: The source node (generates the first part).
2. **Bob**: The repeater node (generates the second part).
3. **Charlie**: The measurement node (generates the final part).

Your goal is to successfully interact with each agent in the correct order to piece together the complete flag.

## Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask application:
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` (or `http://localhost:5000`).

## Usage / API Endpoints

The network consists of three main endpoints corresponding to the agents. You will need to send JSON `POST` requests to interact with them.

### 1. Alice (Transmission)
- **Endpoint**: `/agent/alice`
- **Method**: `POST`
- **Required JSON Payload**:
  - `to`: The name of the target node.
  - `message`: A specific protocol message to initiate transmission.

### 2. Bob (Entanglement Swapping)
- **Endpoint**: `/agent/bob`
- **Method**: `POST`
- **Required JSON Payload**:
  - `to`: The name of the target node.
  - `message`: A specific verification message.
  - `entanglement_id`: The session ID received from Alice.

### 3. Charlie (Measurement)
- **Endpoint**: `/agent/charlie`
- **Method**: `POST`
- **Required JSON Payload**:
  - `response_type`: The type of response required (e.g., "proof").
  - `message`: A specific proof statement.
  - `entanglement_id`: The session ID received from previous steps.

## Status Check
You can check the status of an active entanglement session:
- **Endpoint**: `/status/<entanglement_id>`
- **Method**: `GET`

## Hints & Rules
- **Session Timeout**: Entanglement sessions expire after 5 minutes. If a session expires, you must start over with Alice.
- **Sequence**: You must follow the linear sequence: **Alice → Bob → Charlie**.
- **Error Messages**: Pay close attention to the error messages in the HTTP responses; they contain vital hints about the required messages and parameters!

## Disclaimer
This is a CTF challenge. The "quantum" mechanics are simulated logic puzzles, not real quantum physics.
