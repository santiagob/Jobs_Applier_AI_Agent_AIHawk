"""Test script to verify You.com API integration"""
import yaml
from pathlib import Path
import httpx

def test_you_api():
    """Test if You.com API is working correctly"""
    
    # Load API key from secrets.yaml
    secrets_path = Path("data_folder/secrets.yaml")
    with open(secrets_path, 'r') as f:
        secrets = yaml.safe_load(f)
    
    api_key = secrets.get('llm_api_key')
    
    if not api_key:
        print("Error: No API key found in secrets.yaml")
        return False
    
    print(f"API key loaded: {api_key[:10]}...")
    
    # Test You.com Agent API directly with correct structure
    print("\nTesting You.com Agent API (Express Agent)...")
    try:
        url = "https://api.you.com/v1/agents/runs"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "agent": "express",
            "input": "Say hello in one word",
            "stream": False
        }
        
        print(f"Request URL: {url}")
        print(f"Request payload: {data}")
        
        response = httpx.post(url, headers=headers, json=data, timeout=30)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response received!")
            
            # Extract answer from You.com's response structure
            output = result.get('output', [])
            for item in output:
                if item.get('type') == 'message.answer':
                    answer = item.get('text', '')
                    print(f"API Answer: {answer[:200]}...")
                    print("\n✅ You.com API is working correctly!")
                    return True
            
            print(f"Response structure: {result}")
            return True
        else:
            print(f"API returned error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"API call failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_you_api()
