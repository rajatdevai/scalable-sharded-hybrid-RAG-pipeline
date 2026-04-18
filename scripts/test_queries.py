import requests

API_URL = "http://localhost:8000/query"

TEST_QUERIES = [
    "What is the company budget?",
    "How many vacation days do I get?",
    "Where is the coffee machine?",
    "Tell me about the onboarding process.",
    "Is there a bonus scheme?"
]

def run_tests():
    print(f"Running {len(TEST_QUERIES)} test queries against {API_URL}...\n")
    
    for query in TEST_QUERIES:
        print(f"QUERY: {query}")
        try:
            response = requests.post(API_URL, json={"query": query})
            if response.status_code == 200:
                answer = response.json().get("answer")
                print(f"ANSWER: {answer}\n")
            else:
                print(f"ERROR: {response.status_code} - {response.text}\n")
        except Exception as e:
            print(f"CONNECTION ERROR: {str(e)}\n")

if __name__ == "__main__":
    run_tests()
