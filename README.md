# X-Bot: Twitter Automation Bot

## Description
X-Bot is a Twitter/X automation bot that posts promotional tweets using data stored in Firebase, generates text with AI via Groq Cloud, and sends notifications via SMS with the Twilio API.

## Features
- Retrieves the current index for the post.
- Fetches product information from Firebase.
- Generates promotional text using Groq Cloud.
- Posts the text on Twitter.
- Updates Firebase with the post status.
- Sends SMS notifications via Twilio.

## Prerequisites
- Python 3.12
- Firebase account
- Twilio account
- Groq Cloud account
- Twitter Developer account

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/devgabrielsborges/X-Bot.git
    cd X-Bot
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate  # For Windows
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory with the following variables:
    ```env
    x_apikey=YOUR_TWITTER_API_KEY
    x_apisecret=YOUR_TWITTER_API_SECRET
    x_token=YOUR_TWITTER_ACCESS_TOKEN
    x_tokensecret=YOUR_TWITTER_ACCESS_TOKEN_SECRET
    x_bearertoken=YOUR_TWITTER_BEARER_TOKEN
    twilio_sid=YOUR_TWILIO_SID
    twilio_token=YOUR_TWILIO_AUTH_TOKEN
    number_from=YOUR_TWILIO_PHONE_NUMBER
    number_to=YOUR_PHONE_NUMBER
    firebase_api_key=YOUR_FIREBASE_API_KEY
    firebase_db_url=YOUR_FIREBASE_DB_URL
    ```

## Setting up the Development Container
1. Ensure you have Docker installed on your machine.
2. Open the project in Visual Studio Code.
3. When prompted, reopen the project in the development container.
4. The container will be built using the configuration in `.devcontainer/devcontainer.json`.

Note: The devcontainer is optional and only for development.

## Running the Bot
1. Ensure the initial index is correctly set in Firebase under `actual_index`.
2. Run the main script:
    ```bash
    python src/main.py
    ```

## File Structure
- `src/aux_classes.py`: Contains all auxiliary classes and methods used by the main script.
  - `Product`: Class representing the product and its information.
  - `TwilioAPI`: Class for Twilio API operations.
  - `GroqCloud`: Class for Groq Cloud operations.
- `src/main.py`: Main script that runs the complete automation.
- `src/xbot_class.py`: Contains the main class `Xbot` which handles the overall bot operations.
- `src/cli.py`: Command-line interface for interacting with the bot.

## Dependencies
All dependencies are present in `requirements.txt`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
1. Fork the project.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

For questions or issues, please open an issue in this repository.
