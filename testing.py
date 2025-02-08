import requests
import json

with open("examples/simple-receipt.json", "r") as file:
    receipt_data = json.load(file)

response = requests.post(
    'http://localhost:5050/receipts/process',
    data=json.dumps(receipt_data),
    headers={'Content-Type': 'application/json'}
)

if response.status_code == 200:
    receipt_id = response.json().get('id')
    print(f"Receipt ID: {receipt_id}")

    points_response = requests.get(f'http://localhost:5050/receipts/{receipt_id}/points')

    if points_response.status_code == 200:
        points = points_response.json().get('points')
        print(f"Total Points: {points}")
    else:
        print("Failed to retrieve points. Status Code:", points_response.status_code)
else:
    print("Failed to process receipt. Status Code:", response.status_code)
