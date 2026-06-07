from flask import Flask, request, jsonify

app = Flask(__name__)

NODE_ID = 2
LEADER_ID = 2

ledger = []

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
        "alive": True
    })

@app.route("/status")
def status():

    return jsonify({
        "node": NODE_ID,
        "leader": LEADER_ID,
        "alive": True
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
        port=5001
    )