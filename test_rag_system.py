import asyncio
import requests
import json
from datetime import datetime

def test_chat_endpoints():
    """
    Test script to verify the RAG chatbot system is working properly
    """
    base_url = "http://localhost:8000/api/v1/chat"

    print("Testing RAG Chatbot System...")
    print("=" * 50)

    # Test 1: Normal QA
    print("\n1. Testing normal QA endpoint...")
    try:
        response = requests.post(f"{base_url}/", json={
            "question": "What is Physical AI?",
            "user_id": "test_user_123",
            "language": "en"
        })

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Normal QA successful!")
            print(f"Response: {data['response'][:100]}...")
            print(f"Sources: {len(data['sources'])} found")
        else:
            print(f"❌ Normal QA failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error in normal QA test: {e}")

    # Test 2: Selected text QA
    print("\n2. Testing selected text QA endpoint...")
    try:
        response = requests.post(f"{base_url}/selected", json={
            "question": "Can you elaborate on this concept?",
            "selected_text": "Physical AI represents a paradigm shift in artificial intelligence, moving beyond traditional digital computation to embrace the challenges and opportunities of intelligent systems operating in the physical world.",
            "user_id": "test_user_123",
            "language": "en"
        })

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Selected text QA successful!")
            print(f"Response: {data['response'][:100]}...")
            print(f"Sources: {len(data['sources'])} found")
        else:
            print(f"❌ Selected text QA failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error in selected text QA test: {e}")

    # Test 3: Urdu translation
    print("\n3. Testing Urdu translation...")
    try:
        response = requests.post(f"{base_url}/", json={
            "question": "What is Physical AI?",
            "user_id": "test_user_123",
            "language": "ur"
        })

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Urdu translation successful!")
            print(f"Response length: {len(data['response'])} characters")
        else:
            print(f"❌ Urdu translation failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error in Urdu translation test: {e}")

    # Test 4: Rate limiting (try multiple requests quickly)
    print("\n4. Testing rate limiting...")
    try:
        for i in range(3):
            response = requests.post(f"{base_url}/", json={
                "question": f"Test question {i+1}",
                "user_id": "test_user_123",
                "language": "en"
            })
            print(f"   Request {i+1}: Status {response.status_code}")

        print("✅ Rate limiting test completed (check if limits are enforced)")
    except Exception as e:
        print(f"❌ Error in rate limiting test: {e}")

    # Test 5: Capabilities endpoint
    print("\n5. Testing capabilities endpoint...")
    try:
        response = requests.get(f"{base_url}/capabilities")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Capabilities endpoint successful!")
            print(f"Capabilities: {len(data.get('capabilities', []))} features")
            print(f"Supported languages: {data.get('supported_languages', [])}")
        else:
            print(f"❌ Capabilities endpoint failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error in capabilities test: {e}")

    print("\n" + "=" * 50)
    print("Testing completed!")

if __name__ == "__main__":
    test_chat_endpoints()