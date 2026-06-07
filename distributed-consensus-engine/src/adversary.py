from flask import Flask, jsonify

app = Flask(__name__)

NODE_ID = 6

@app.route("/")
def home():
    return "Adversary Node Running"

@app.route("/status")
def status():
    return jsonify({
        "node": NODE_ID,
        "role": "Adversary",
        "alive": True,
        "behavior": "Sending inconsistent messages"
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5005
    )