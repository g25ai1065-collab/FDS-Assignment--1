import requests
import time

while True:

    print("\n========== CLUSTER STATUS ==========")

    # Leader Information
    try:
        leader_response = requests.get(
            "http://localhost:5001/leader",
            timeout=2
        )

        leader_data = leader_response.json()

        print(f"👑 CURRENT LEADER : Node {leader_data['leader']}")

    except Exception as e:

        print("👑 CURRENT LEADER : UNKNOWN")

    print("------------------------------------")

    # Heartbeats
    for port in [5001, 5002, 5003, 5004, 5005]:

        try:

            requests.get(
                f"http://localhost:{port}",
                timeout=2
            )

            print(f"❤️ Node {port-5000} : ALIVE")

        except:

            print(f"💔 Node {port-5000} : DOWN")

    print("====================================")

    time.sleep(5)