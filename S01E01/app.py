import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv
import webbrowser
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Get base URL from environment
BASE_URL = os.getenv('BASE_URL')

def get_question():
    # Get the login page
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print the HTML content to see the structure
    print("HTML content:", response.text)
    
    # Try to find the question - first attempt with a more general approach
    question_element = soup.find('div', class_='question')
    if question_element is None:
        # If not found, try to find any text that looks like a question
        question_element = soup.find(string=lambda text: text and '?' in text)
    
    if question_element is None:
        raise Exception("Could not find the question on the page. Please check the HTML structure.")
    
    # If we found a string directly, use it, otherwise get the text from the element
    question = question_element if isinstance(question_element, str) else question_element.text.strip()
    return question

def get_llm_answer(question):
    # Get answer from GPT using the new API format
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions concisely. Answer the question in ne word"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()

def login(username, password, answer):
    # Prepare the login data
    data = {
        'username': username,
        'password': password,
        'answer': answer
    }
    
    # Set headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Create request
    request = requests.Request('POST', BASE_URL, data=data, headers=headers)
    prepared_request = request.prepare()
    
    # Print the request body
    print("Request body:", prepared_request.body)
    
    # Send POST request
    response = requests.post(BASE_URL, data=data, headers=headers)
    return response

def extract_url_from_response(response_text):
    # Try to find URL in the response text
    # This pattern looks for URLs starting with http:// or https://
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(url_pattern, response_text)
    if match:
        return match.group(0)
    return None

def main():
    username = 'tester'
    password = '574e112a'
    
    # Get the current question
    question = get_question()
    print(f"Current question: {question}")
    
    # Get answer from LLM
    answer = get_llm_answer(question)
    print(f"LLM answer: {answer}")
    
    # Attempt login
    response = login(username, password, answer)
    
    # Check if login was successful
    if response.status_code == 200:
        print("Login successful!")
        
        # Save HTML response to a file
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("HTML response saved to response.html")
        
        # Open the HTML file in browser
        webbrowser.open('file://' + os.path.abspath('response.html'))
    else:
        print(f"Login failed with status code: {response.status_code}")
        print("Response content:", response.text)

if __name__ == "__main__":
    main() 