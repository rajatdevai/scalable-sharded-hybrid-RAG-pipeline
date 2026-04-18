import os
import requests
import time

API_URL = "http://localhost:8000/ingest"
SAMPLE_DOCS_PATH = os.path.join("data", "sample_docs")

def load_data():
    if not os.path.exists(SAMPLE_DOCS_PATH):
        print(f"Error: {SAMPLE_DOCS_PATH} not found.")
        return

    with open(SAMPLE_DOCS_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"Found {len(lines)} documents to ingest.")
    
    payload = {"documents": lines}
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Successfully queued documents for ingestion!")
            print(f"Response: {response.json()}")
        else:
            print(f"Failed to ingest. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
        print("Make sure the FastAPI server is running on http://localhost:8000")

if __name__ == "__main__":
    load_data()
