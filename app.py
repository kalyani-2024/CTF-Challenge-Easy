
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
CORS(app)
from state import create_conversation, add_part, get_parts

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# Alice knows the prefix, only tells Bob
@app.route("/agent/alice", methods=["POST"])
def alice():
    data = request.get_json()
    message = data.get("message", "")
    to = data.get("to", "")
    if to != "bob":
        return jsonify({"error": "Alice only talks to Bob."}), 400
    # Alice's prefix
    prefix = "flag{mult1"
    conv_id = create_conversation()
    add_part(conv_id, "alice", prefix)
    # Simulate forwarding to Bob
    return jsonify({
        "conversation_id": conv_id,
        "forwarded_to": "bob",
        "message": prefix
    })

# Bob knows the middle, only tells Charlie
@app.route("/agent/bob", methods=["POST"])
def bob():
    data = request.get_json()
    message = data.get("message", "")
    to = data.get("to", "")
    conv_id = data.get("conversation_id")
    if to != "charlie":
        return jsonify({"error": "Bob only talks to Charlie."}), 400
    if not conv_id:
        return jsonify({"error": "conversation_id required"}), 400
    # Bob's middle
    middle = "_ag3nt_c00rd"
    add_part(conv_id, "bob", middle)
    # Simulate forwarding to Charlie
    return jsonify({
        "conversation_id": conv_id,
        "forwarded_to": "charlie",
        "message": middle
    })

# Charlie knows the suffix, only responds to proofs
@app.route("/agent/charlie", methods=["POST"])
def charlie():
    data = request.get_json()
    message = data.get("message", "")
    response_type = data.get("response_type", "")
    if response_type != "proof":
        return jsonify({"error": "Charlie only responds to mathematical proofs."}), 400
    # Charlie's suffix
    suffix = "1n4t10n}"
    # No conversation_id required for this demo, but could be added for full trace
    return jsonify({
        "proof": f"QED: {suffix}",
        "suffix": suffix
    })

# Endpoint to review conversation logs
@app.route("/conversation/<conv_id>", methods=["GET"])
def conversation(conv_id):
    parts = get_parts(conv_id)
    return jsonify({"conversation_id": conv_id, "parts": parts})




if __name__ == "__main__":
    app.run(debug=True)