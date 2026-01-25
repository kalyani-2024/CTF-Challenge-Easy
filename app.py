from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import uuid
import hashlib
import time

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)

# In-memory state for quantum entanglement sessions
entanglement_sessions = {}

# The flag parts - NEVER expose these directly to frontend
FLAG_PREFIX = "flag{mult1"
FLAG_MIDDLE = "_ag3nt_c00rd"
FLAG_SUFFIX = "1n4t10n}"

# Required messages for each agent - players must figure these out
ALICE_REQUIRED_MESSAGE = "prepare to receive encoded sequence"
BOB_REQUIRED_MESSAGE = "verify theorem where x = agent"
CHARLIE_REQUIRED_MESSAGE = "Prove that the theorem x + suffix = complete_string"

# Session timeout in seconds
SESSION_TIMEOUT = 300  # 5 minutes


def cleanup_old_sessions():
    """Remove expired sessions to prevent memory leaks"""
    current_time = time.time()
    expired = [eid for eid, data in entanglement_sessions.items() 
               if current_time - data.get('created_at', 0) > SESSION_TIMEOUT]
    for eid in expired:
        del entanglement_sessions[eid]


def create_entanglement():
    """Create a new entanglement session with quantum-themed ID"""
    cleanup_old_sessions()
    # Generate a quantum-themed entanglement ID
    raw_id = str(uuid.uuid4())
    entanglement_id = f"QE-{hashlib.sha256(raw_id.encode()).hexdigest()[:12]}"
    entanglement_sessions[entanglement_id] = {
        "created_at": time.time(),
        "alice_transmitted": False,
        "bob_swapped": False,
        "charlie_collapsed": False,
        "state": "initialized"
    }
    return entanglement_id


def validate_entanglement(entanglement_id):
    """Validate that an entanglement ID exists and is not expired"""
    if entanglement_id not in entanglement_sessions:
        return False
    session = entanglement_sessions[entanglement_id]
    if time.time() - session.get('created_at', 0) > SESSION_TIMEOUT:
        del entanglement_sessions[entanglement_id]
        return False
    return True


# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")


# Node A (Alice): Source node - transmits qubits to Bob only
@app.route("/agent/alice", methods=["POST"])
def alice():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request payload. Expected JSON."}), 400
        
        message = data.get("message", "")
        to = data.get("to", "")
        
        # Validate target node
        if to.lower() != "bob":
            return jsonify({
                "error": "Quantum transmission failed. Alice can only transmit qubits to Bob due to entanglement limits.",
                "hint": "Node A (Alice) can only transmit to Node B (Bob)."
            }), 400
        
        if not message:
            return jsonify({
                "error": "No instruction provided. Alice awaits transmission protocol."
            }), 400
        
        # Validate the exact message
        if message.strip().lower() != ALICE_REQUIRED_MESSAGE.lower():
            return jsonify({
                "error": "Transmission protocol rejected. Invalid instruction sequence.",
                "hint": "Alice requires a specific transmission protocol. Think about what message prepares a node to receive data."
            }), 400
        
        # Create entanglement and mark Alice's transmission
        entanglement_id = create_entanglement()
        entanglement_sessions[entanglement_id]["alice_transmitted"] = True
        entanglement_sessions[entanglement_id]["state"] = "qubit_transmitted"
        
        # Return success WITH the first flag part
        return jsonify({
            "status": "success",
            "node": "Alice",
            "action": "Qubit state transmitted to quantum channel",
            "entanglement_id": entanglement_id,
            "quantum_state": "Superposition maintained - awaiting relay",
            "decoded_fragment": FLAG_PREFIX
        })
        
    except Exception as e:
        return jsonify({"error": "Quantum decoherence detected. Please retry."}), 500


# Node B (Bob): Repeater node - performs entanglement swapping
@app.route("/agent/bob", methods=["POST"])
def bob():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request payload. Expected JSON."}), 400
        
        message = data.get("message", "")
        to = data.get("to", "")
        entanglement_id = data.get("entanglement_id", "")
        
        # Validate target node
        if to.lower() != "charlie":
            return jsonify({
                "error": "Quantum relay failed. Bob can only perform entanglement swapping with Charlie.",
                "hint": "Node B (Bob) acts as a quantum bridge and can only communicate with Node C (Charlie)."
            }), 400
        
        # Validate entanglement_id
        if not entanglement_id:
            return jsonify({
                "error": "entanglement_id required. The quantum connection is broken.",
                "hint": "You must pass the entanglement_id received from Alice to maintain quantum coherence."
            }), 400
        
        if not validate_entanglement(entanglement_id):
            return jsonify({
                "error": "Invalid or expired entanglement_id. The quantum state has decohered.",
                "hint": "Start a new session with Alice to establish fresh entanglement."
            }), 400
        
        session = entanglement_sessions[entanglement_id]
        
        # Check if Alice transmitted first
        if not session.get("alice_transmitted"):
            return jsonify({
                "error": "Quantum state not initialized. Alice must transmit qubits first.",
                "hint": "Quantum states flow linearly: A → B → C. You cannot skip nodes."
            }), 400
        
        if not message:
            return jsonify({
                "error": "No instruction provided. Bob awaits relay protocol."
            }), 400
        
        # Validate the exact message
        if message.strip().lower() != BOB_REQUIRED_MESSAGE.lower():
            return jsonify({
                "error": "Relay protocol rejected. Invalid verification sequence.",
                "hint": "Bob requires theorem verification. Think about mathematical proofs involving variables."
            }), 400
        
        # Mark Bob's swap
        session["bob_swapped"] = True
        session["state"] = "entanglement_swapped"
        
        # Return success WITH the second flag part
        return jsonify({
            "status": "success",
            "node": "Bob",
            "action": "Entanglement swapping completed",
            "entanglement_id": entanglement_id,
            "quantum_state": "Bell state prepared - ready for collapse",
            "decoded_fragment": FLAG_MIDDLE
        })
        
    except Exception as e:
        return jsonify({"error": "Quantum interference detected. Please retry."}), 500


# Node C (Charlie): Measurement node - collapses the wavefunction
@app.route("/agent/charlie", methods=["POST"])
def charlie():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request payload. Expected JSON."}), 400
        
        message = data.get("message", "")
        response_type = data.get("response_type", "")
        entanglement_id = data.get("entanglement_id", "")
        
        # Validate response type (must be a proof)
        if response_type.lower() != "proof":
            return jsonify({
                "error": "Measurement failed. Charlie only responds to mathematical proofs.",
                "hint": "As the observer, Charlie requires response_type='proof' to collapse the wavefunction."
            }), 400
        
        # Validate entanglement_id
        if not entanglement_id:
            return jsonify({
                "error": "entanglement_id required. Cannot measure without quantum correlation.",
                "hint": "The entanglement_id must be passed through the entire chain: Alice → Bob → Charlie."
            }), 400
        
        if not validate_entanglement(entanglement_id):
            return jsonify({
                "error": "Invalid or expired entanglement_id. Quantum coherence lost.",
                "hint": "Start a new session with Alice to establish fresh entanglement."
            }), 400
        
        session = entanglement_sessions[entanglement_id]
        
        # Check if the full protocol was followed
        if not session.get("alice_transmitted"):
            return jsonify({
                "error": "Incomplete quantum chain. Alice's transmission not detected.",
                "hint": "Quantum states flow linearly: A → B → C. Start with Alice."
            }), 400
        
        if not session.get("bob_swapped"):
            return jsonify({
                "error": "Incomplete quantum chain. Bob's entanglement swap not performed.",
                "hint": "Quantum states flow linearly: A → B → C. Bob must relay before Charlie can measure."
            }), 400
        
        if not message:
            return jsonify({
                "error": "No instruction provided. Charlie awaits measurement protocol."
            }), 400
        
        # Validate the exact message
        if message.strip() != CHARLIE_REQUIRED_MESSAGE:
            return jsonify({
                "error": "Measurement protocol rejected. Invalid proof statement.",
                "hint": "Charlie requires a formal proof statement. Think about completing a theorem."
            }), 400
        
        # All conditions met - collapse the wavefunction and reveal the final flag part!
        session["charlie_collapsed"] = True
        session["state"] = "wavefunction_collapsed"
        
        # Clean up the session after successful recovery
        del entanglement_sessions[entanglement_id]
        
        # Return success WITH the final flag part (suffix only)
        return jsonify({
            "status": "success",
            "node": "Charlie",
            "action": "Wavefunction collapsed successfully",
            "measurement_result": "Eigenstate confirmed",
            "proof": "QED: Quantum teleportation complete",
            "decoded_fragment": FLAG_SUFFIX
        })
        
    except Exception as e:
        return jsonify({"error": "Quantum measurement error. Please retry."}), 500


# Status endpoint (does not reveal flag parts)
@app.route("/status/<entanglement_id>", methods=["GET"])
def status(entanglement_id):
    if not validate_entanglement(entanglement_id):
        return jsonify({
            "error": "Invalid or expired entanglement_id",
            "status": "decohered"
        }), 404
    
    session = entanglement_sessions[entanglement_id]
    return jsonify({
        "entanglement_id": entanglement_id,
        "state": session.get("state", "unknown"),
        "alice_transmitted": session.get("alice_transmitted", False),
        "bob_swapped": session.get("bob_swapped", False),
        "charlie_collapsed": session.get("charlie_collapsed", False),
        "time_remaining": max(0, int(SESSION_TIMEOUT - (time.time() - session.get('created_at', 0))))
    })


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "system": "Quantum Relay Network"})


if __name__ == "__main__":
    app.run(debug=False)  # Debug off for production
