# X-Bot: Twitter Automation Bot

## Description
X-Bot is a Twitter/X automation bot that posts promotional tweets using data stored in Firebase, generates text with AI via Groq Cloud, and sends notifications via SMS with the Twilio API.

## Features
- Retrieves the current index for the post
- Fetches product information from Firebase
- Generates promotional text using Groq Cloud's AI models
- Posts the text on Twitter/X
- Updates Firebase with the post status
- Sends SMS notifications via Twilio

## Prerequisites
- Python 3.12
- Poetry (Python dependency management)
- Firebase account and credentials.json file
- Twilio account
- Groq Cloud account
- Twitter Developer account

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/devgabrielsborges/X-Bot.git
    cd X-Bot
    ```
2. Install dependencies with Poetry:
    ```bash
    # Install Poetry if you don't have it
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Install dependencies
    poetry install
    
    # Activate the virtual environment
    poetry shell
    ```
3. Create a `.env` file in the root directory with the following variables:
    ```env
    FIREBASE_URL=YOUR_FIREBASE_DB_URL
    TWILIO_SID=YOUR_TWILIO_SID
    TWILIO_TOKEN=YOUR_TWILIO_AUTH_TOKEN
    NUMBER_FROM=YOUR_TWILIO_PHONE_NUMBER
    NUMBER_TO=YOUR_PHONE_NUMBER
    X_BEARERTOKEN=YOUR_TWITTER_BEARER_TOKEN
    X_APIKEY=YOUR_TWITTER_API_KEY
    X_APISECRET=YOUR_TWITTER_API_SECRET
    X_TOKEN=YOUR_TWITTER_ACCESS_TOKEN
    X_TOKENSECRET=YOUR_TWITTER_ACCESS_TOKEN_SECRET
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    ```

4. Place your Firebase [credentials.json](http://_vscodecontentref_/0) file in the project root directory.

## Running the Bot
1. Ensure the initial index is correctly set in Firebase under `actual_index`.
2. Run the main script:
    ```bash
    # Using Poetry script
    poetry run xbot
    
    # Or if you've already activated the environment with 'poetry shell'
    xbot
    ```

3. Run with a specific item index (using CLI):
    ```bash
    poetry run python -m src.x_bot.cli 3
    ```

## Running Tests
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_product.py

# Run with verbose output
poetry run pytest -v