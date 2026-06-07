import requests

tx = input("Transaction: ")

response = requests.post(
    "http://localhost:5001/preprepare",
    json={
        "tx": tx
    }
)

print(response.json())