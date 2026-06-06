
from flask import Flask, request, jsonify

app = Flask(__name__)

NODE_ID = 5

ledger = []

@app.route("/")
def home():
    return f"Node {NODE_ID} is running"

@app.route("/transaction", methods=["POST"])
def transaction():

    data = request.json

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