import requests
import json
import os
from typing import Dict, Any
from prompts import VerificationPrompts
from openai_service import OpenAIService
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class VerificationBot:
    def __init__(self, base_url: str = None, openai_api_key: str = None):
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        if not base_url:
            raise ValueError("Base URL is required")
        self.base_url = base_url
        self.verify_endpoint = f"{base_url}/verify"
        self.headers = {
            "Content-Type": "application/json"
        }
        self.openai_service = OpenAIService(openai_api_key)

    def start_verification(self) -> Dict[str, Any]:
        """Start the verification process by sending READY command."""
        payload = {
            "text": "READY",
            "msgID": "0"
        }
        print("\n=== Starting Verification ===")
        print(f"Sending initial payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            self.verify_endpoint,
            headers=self.headers,
            json=payload
        )
        response_data = response.json()
        print(f"Received response: {json.dumps(response_data, indent=2)}")
        return response_data

    def send_response(self, message_id: str, response: str) -> Dict[str, Any]:
        """Send response to the verification bot."""
        print(f"\n=== Sending Response ===")
        print(f"Message ID: {message_id}")
        print(f"Response payload: {response}")
        
        response = requests.post(
            self.verify_endpoint,
            headers=self.headers,
            json=json.loads(response)  # Parse the JSON string from LLM
        )
        response_data = response.json()
        print(f"Received response: {json.dumps(response_data, indent=2)}")
        return response_data

    def get_llm_response(self, question: str, message_id: str) -> str:
        """Get response from OpenAI based on the question and context."""
        print(f"\n=== Getting LLM Response ===")
        print(f"Question: {question}")
        print(f"Message ID: {message_id}")
        
        response = self.openai_service.get_verification_response(
            question=question,
            message_id=message_id
        )
        print(f"LLM Response: {response}")
        return response

    def process_verification(self):
        """Main method to handle the verification process."""
        try:
            print("\n=== Starting Verification Process ===")
            # Start verification
            initial_response = self.start_verification()
            print("\n=== Initial Response Received ===")
            print(f"Full initial response: {json.dumps(initial_response, indent=2)}")

            current_response = initial_response
            while True:
                # Extract message_id and question from response
                message_id = current_response.get("msgID")
                question = current_response.get("text")
                
                print(f"\n=== Processing New Message ===")
                print(f"Message ID: {message_id}")
                print(f"Question: {question}")
                
                if not message_id or not question:
                    print("Error: Missing message_id or question in response")
                    print(f"Current response: {json.dumps(current_response, indent=2)}")
                    break
                
                # Check if we received the flag
                if "FLG" in current_response:
                    print(f"\n=== SUCCESS! ===")
                    print(f"Flag received: {current_response['flag']}")
                    break
                
                # Generate response using LLM
                llm_response = self.get_llm_response(question, message_id)
                print(f"\n=== Generated Response ===")
                print(f"Response: {llm_response}")
                
                # Send response and get next question
                current_response = self.send_response(message_id, llm_response)
                
        except Exception as e:
            print(f"\n=== ERROR OCCURRED ===")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Full error details: {e}")

def main():
    # Get OpenAI API key from environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Get Base URL from environment variable
    BASE_URL = os.getenv("BASE_URL")
    if not BASE_URL:
        raise ValueError("BASE_URL environment variable is not set")
    
    bot = VerificationBot(base_url=BASE_URL, openai_api_key=OPENAI_API_KEY)
    bot.process_verification()

if __name__ == "__main__":
    main() 