# Robot Login Automation

This script automates the login process for the robot system.

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the same directory with your OpenAI API key and base URL:
```
OPENAI_API_KEY=your_api_key_here
BASE_URL=https://xyz.ag3nts.org/
```

**Note**: Replace `your_api_key_here` with your actual OpenAI API key from https://platform.openai.com/api-keys

## Usage

Run the script:
```bash
python app.py
```

The script will:
1. Fetch the current question from the login page
2. Send the question to GPT-4 for an answer
3. Attempt to log in with the provided credentials and the LLM's answer
4. Display the response from the server

## Configuration

The script uses the following environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4 access
- `BASE_URL`: The URL of the robot system (e.g., https://xyz.ag3nts.org/)

And the following hardcoded credentials:
- Username: tester
- Password: 574e112a

Make sure you have a valid OpenAI API key and BASE_URL in your `.env` file before running the script. 