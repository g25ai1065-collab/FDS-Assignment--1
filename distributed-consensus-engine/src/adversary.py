import requests

tx = "MALICIOUS_TRANSACTION"

for port in [5001, 5002, 5003, 5004, 5005]:

    try:

        response = requests.post(
            f"http://localhost:{port}/prepare_pbft",
            json={"tx": tx},
            timeout=2
        )

        print(
            f"Sent forged PBFT message to node on port {port}"
        )

    except Exception as e:

        print(e)
        