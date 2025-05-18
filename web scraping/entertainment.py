import requests

API_URL = "api_url"
API_TOKEN = "your_api_token_here"  # Replace 'your_api_token_here' with your actual API token

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "Can you please let us know more details about your",
})
print(output)
