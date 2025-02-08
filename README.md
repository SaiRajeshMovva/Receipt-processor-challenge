# Receipt Processor API

## Overview
This **Receipt Processor API** allows users to submit receipts in JSON format and calculate points based on predefined rules.

## Features
- **Process Receipts**: Submit a receipt and receive a unique ID.
- **Retrieve Points**: Fetch points for a processed receipt using its ID.
- **Stateless Design**: Data is stored in memory and does not persist after restart.

## Tech Stack
- **Language**: Python 3.10
- **Framework**: Flask
- **Containerization**: Docker
- **Testing**: `curl` for API testing

---

## Getting Started

### Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [cURL](https://curl.se/download.html) (for testing via command line)

---

## Running the Application with Docker

### 1. Clone the repo 
```sh
git clone https://github.com/SaiRajeshMovva/Receipt-processor-challenge && cd Receipt-processor-challenge
```

### 2. Build the Docker Image
Run the following command in the project root:
```sh
docker build -t receipt-processor .
```

### 3. Run the Docker Container (Bind local port 5050)
```sh
docker run -p 5050:5050 receipt-processor
```
- The API will now be available at `http://localhost:5050/`

---

## API Endpoints

### **1. Process a Receipt**
- **Endpoint**: `POST /receipts/process`
- **Description**: Submits a receipt JSON and returns a unique receipt ID.
- **Request Example**:
```sh
curl -X POST "http://localhost:5050/receipts/process" \
     -H "Content-Type: application/json" \
     -d @receipt.json  # Ensure correct path
```

- **Response Example**:
```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### **2. Get Points for a Receipt**
- **Endpoint**: `GET /receipts/{id}/points`
- **Description**: Retrieves the points awarded for a given receipt ID.
- **Request Example**:
```sh
curl -X GET "http://localhost:5050/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points"
```

- **Response Example**:
```json
{
  "points": 32
}
```

---
## Additional Info

- API Endpoint can also be verified using python as shown in `testing.py`.
- The API runs **in-memory**, meaning receipts are lost when the app restarts.
- Uses `uuid` for generating unique receipt IDs.

---

## Author
**Sai Rajesh Movva**

