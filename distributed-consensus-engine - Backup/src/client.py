import requests

transaction = {
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 200
}

response = requests.post(
    "http://127.0.0.1:5000/transaction",
    json=transaction
)

print(response.json())