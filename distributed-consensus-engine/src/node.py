from flask import Flask, request, jsonify
import requests
import os
from crypto_utils import generate_keys, sign_message

app = Flask(__name__)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

NODE_ID = os.environ.get("NODE_ID", "1")
NODE_ID_INT = int(NODE_ID)

PEERS = [
    "http://node1:5000",
    "http://node2:5000",
    "http://node3:5000",
    "http://node4:5000",
    "http://node5:5000"
]

LEADER_ID = 5

PROMISED_ID = -1
ACCEPTED_ID = -1

PRIVATE_KEY, PUBLIC_KEY = generate_keys()

# --------------------------------------------------
# LEADER ELECTION
# --------------------------------------------------

def elect_leader():

    global LEADER_ID

    active_nodes = []

    for peer_id in [1, 2, 3, 4, 5]:

        try:

            requests.get(
                f"http://node{peer_id}:5000/",
                timeout=1
            )

            active_nodes.append(peer_id)

        except:
            pass

    if active_nodes:
        LEADER_ID = max(active_nodes)

    print(
        f"Current Leader = Node {LEADER_ID}",
        flush=True
    )


@app.route("/leader")
def leader():

    return jsonify({
        "leader": LEADER_ID
    })


@app.route("/elect")
def run_election():

    elect_leader()

    return jsonify({
        "leader": LEADER_ID
    })

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/")
def home():

    return f"Node {NODE_ID} Alive"

# --------------------------------------------------
# TRANSACTION ENTRY POINT
# --------------------------------------------------

@app.route("/transaction", methods=["POST"])
def transaction():

    tx = request.json["tx"]

    print(
        f"[NODE {NODE_ID}] RECEIVED TRANSACTION {tx}",
        flush=True
    )

    if NODE_ID_INT != LEADER_ID:

        try:

            response = requests.post(
                f"http://node{LEADER_ID}:5000/preprepare",
                json={
                    "tx": tx
                },
                timeout=5
            )

            return jsonify(response.json())

        except Exception:

            return jsonify({
                "status": "LEADER_UNAVAILABLE"
            }), 503

    return preprepare()

# --------------------------------------------------
# PAXOS
# --------------------------------------------------

@app.route("/prepare", methods=["POST"])
def prepare():

    global PROMISED_ID

    proposal_id = request.json["proposal_id"]

    if proposal_id > PROMISED_ID:

        PROMISED_ID = proposal_id

        print(
            f"Node {NODE_ID}: PROMISE {proposal_id}",
            flush=True
        )

        return jsonify({
            "status": "PROMISE",
            "node": NODE_ID
        })

    return jsonify({
        "status": "REJECT"
    })


@app.route("/accept", methods=["POST"])
def accept():

    global ACCEPTED_ID

    proposal_id = request.json["proposal_id"]

    if proposal_id >= PROMISED_ID:

        ACCEPTED_ID = proposal_id

        print(
            f"Node {NODE_ID}: ACCEPTED {proposal_id}",
            flush=True
        )

        return jsonify({
            "status": "ACCEPTED",
            "node": NODE_ID
        })

    return jsonify({
        "status": "REJECT"
    })


@app.route("/propose", methods=["POST"])
def propose():

    proposal_id = request.json["proposal_id"]

    promises = 0

    for peer in PEERS:

        try:

            response = requests.post(
                f"{peer}/prepare",
                json={
                    "proposal_id": proposal_id
                },
                timeout=2
            )

            if response.json()["status"] == "PROMISE":
                promises += 1

        except:
            pass

    if promises >= 3:

        accepted = 0

        for peer in PEERS:

            try:

                response = requests.post(
                    f"{peer}/accept",
                    json={
                        "proposal_id": proposal_id
                    },
                    timeout=2
                )

                if response.json()["status"] == "ACCEPTED":
                    accepted += 1

            except:
                pass

        if accepted >= 3:

            print(
                "PAXOS CONSENSUS REACHED",
                flush=True
            )

            return jsonify({
                "status": "COMMITTED"
            })

    return jsonify({
        "status": "FAILED"
    })

# --------------------------------------------------
# PBFT
# --------------------------------------------------

@app.route("/preprepare", methods=["POST"])
def preprepare():

    tx = request.json["tx"]

    signature = sign_message(
        PRIVATE_KEY,
        tx
    )

    print(
        f"[NODE {NODE_ID}] PRE-PREPARE {tx}",
        flush=True
    )

    for peer in PEERS:

        try:

            requests.post(
                f"{peer}/prepare_pbft",
                json={
                    "tx": tx,
                    "signature": signature.hex()
                },
                timeout=2
            )

        except:
            pass

    return jsonify({
        "status": "PREPREPARE_SENT"
    })


@app.route("/prepare_pbft", methods=["POST"])
def prepare_pbft():

    tx = request.json["tx"]

    print(
        f"[NODE {NODE_ID}] PREPARE {tx}",
        flush=True
    )

    try:

        requests.post(
            "http://node1:5000/commit_pbft",
            json={
                "tx": tx
            },
            timeout=2
        )

    except:
        pass

    return jsonify({
        "status": "PREPARED"
    })


@app.route("/commit_pbft", methods=["POST"])
def commit_pbft():

    tx = request.json["tx"]

    print(
        f"[NODE {NODE_ID}] COMMIT {tx}",
        flush=True
    )

    print(
        f"*** PBFT EXECUTED ON NODE {NODE_ID}: {tx} ***",
        flush=True
    )

    return jsonify({
        "status": "COMMITTED"
    })

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    elect_leader()

    app.run(
        host="0.0.0.0",
        port=5000
    )