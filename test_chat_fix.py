import requests
import json
import time

# Wait a bit for the server to start
time.sleep(3)

def test_chat_endpoint():
    url = "http://127.0.0.1:8000/api/test_user/chat"
    
    # Test message that should trigger the agent to add a task
    payload = {
        "message": "Add a task to buy groceries"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Check if the response is meaningful and not just an echo
        response_data = response.json()
        if "response" in response_data:
            response_text = response_data["response"]
            if response_text.startswith("Echo:"):
                print("\n❌ ERROR: Still echoing! The fix didn't work.")
                print(f"Response was: {response_text}")
            else:
                print("\n✅ SUCCESS: The response is no longer an echo!")
                print(f"Response was: {response_text}")
        else:
            print(f"\n⚠️  Unexpected response format: {response_data}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    print("Testing the chat endpoint to verify the echo issue is fixed...")
    test_chat_endpoint()