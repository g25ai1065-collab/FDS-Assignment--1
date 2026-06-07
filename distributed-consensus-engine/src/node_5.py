from flask import Flask, request, jsonify

app = Flask(__name__)

NODE_ID = 5
LEADER_ID = 1

ledger = []

NODE_ALIVE = True

@app.route("/")
def home():
    return f"Node {NODE_ID} is running"

@app.route("/leader")
def leader():
    return jsonify({
        "leader": LEADER_ID,
        "node": NODE_ID
    })

@app.route("/heartbeat")
def heartbeat():
    return jsonify({
        "node": NODE_ID,
        "alive": NODE_ALIVE
    })

@app.route("/status")
def status():
    return jsonify({
        "node": NODE_ID,
        "leader": LEADER_ID,
        "alive": NODE_ALIVE
    })

@app.route("/fail")
def fail_node():
    global NODE_ALIVE
    NODE_ALIVE = False

    return jsonify({
        "node": NODE_ID,
        "status": "FAILED"
    })

@app.route("/recover")
def recover_node():
    global NODE_ALIVE
    NODE_ALIVE = True

    return jsonify({
        "node": NODE_ID,
        "status": "RECOVERED"
    })

@app.route("/transaction", methods=["POST"])
def transaction():
    data = request.get_json()

    ledger.append(data)

    return jsonify({
        "status": "committed",
        "ledger": ledger
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5004
    )