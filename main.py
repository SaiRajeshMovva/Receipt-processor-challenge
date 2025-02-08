from flask import Flask, request, jsonify
from uuid import uuid4
from math import ceil
from datetime import datetime, time


app = Flask(__name__)

receipts = {}

def calculate_points(receipt):
    points = 0

    # 1. One point for every alphanumeric character in the retailer name.
    retailer = receipt.get('retailer', '')
    points += sum(char.isalnum() for char in retailer)

    # 2. 50 points if the total is a round dollar amount with no cents.
    total = float(receipt.get('total', '0.00'))
    if total.is_integer():
        points += 50

    # 3. 25 points if the total is a multiple of 0.25.
    if total % 0.25 == 0:
        points += 25

    # 4. 5 points for every two items on the receipt.
    items = receipt.get('items', [])
    points += (len(items) // 2) * 5

    # 5. If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in items:
        description = item.get('shortDescription', '').strip()
        if len(description) % 3 == 0:
            price = float(item.get('price', '0.00'))
            points += ceil(price * 0.2)

    # 6. 6 points if the day in the purchase date is odd.
    purchase_date = receipt.get('purchaseDate', '')
    try:
        day = int(purchase_date.split('-')[2])
        if day % 2 != 0:
            points += 6
    except (IndexError, ValueError):
        pass

    # 7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time_str = receipt.get('purchaseTime', '')
    try:
        purchase_time = datetime.strptime(purchase_time_str, '%H:%M').time()
        start_time = time(14, 0)  # 2:00 PM
        end_time = time(16, 0)    # 4:00 PM
        if start_time < purchase_time < end_time:
            points += 10
    except ValueError:
        pass

    return points


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.json
    receipt_id = str(uuid4())
    points = calculate_points(receipt)
    receipts[receipt_id] = points
    return jsonify({"id": receipt_id}), 200


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts.get(receipt_id)
    if points is not None:
        return jsonify({"points": points}), 200
    else:
        return jsonify({"error": "Receipt not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
