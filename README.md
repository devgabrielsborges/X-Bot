## _A X (Twitter) bot_ 

# X-Bot Automation

This repository contains a bot that automates posting tweets about promotions, using information from an Excel spreadsheet, generating text with AI via Groq Cloud, and sending notifications via SMS with the Twilio API.

## Features

1. **Retrieves the current index for the post**.
2. **Fetches product information from the Excel spreadsheet**.
3. **Generates a promotional text for the product using Groq Cloud**.
4. **Posts the text on Twitter**.
5. **Updates the spreadsheet with the post status**.
6. **Sends an SMS notification via Twilio**.

## Prerequisites

- Python 3.8+
- Firebase account
- Twilio account
- Groq Cloud account
- Twitter Developer account

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/devgabrielsborges/X-Bot.git
    cd X-Bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate  # For Windows
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root of the project with the following variables:
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
    ```

5. Set up your Excel spreadsheet (`Projeto-X-Bot.xlsx`) in the expected format:
    - Column A: Product name
    - Column B: Product price
    - Column C: Product link

## Running the Bot

1. Ensure that the initial index is correctly set in Firebase under `actual_index`.

2. Run the main script:
    ```sh
    python main.py
    ```

## File Structure

- `classes.py`: Contains all the auxiliary classes and methods used by the main script.
    - `SheetXlsx`: Class for operations with Excel spreadsheets.
    - `FirebaseAPI`: Class for operations with Firebase.
    - `TwilioAPI`: Class for operations with the Twilio API.
    - `GroqCloud`: Class for operations with Groq Cloud.
- `main.py`: Main script that runs the complete automation.

## Dependencies

- `openpyxl`: For Excel spreadsheet manipulation.
- `pytz`: For timezone manipulation.
- `requests`: For HTTP requests.
- `tweepy`: For interacting with the Twitter API.
- `python-dotenv`: For loading environment variables from a `.env` file.
- `twilio`: For sending SMS via Twilio.
- `langchain_core` and `langchain_groq`: For integration with Groq Cloud.

## License

This project is licensed under the [MIT License](LICENSE).

## Contribution

1. Fork the project
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a new Pull Request

---

For any questions or issues, please open an issue in this repository.

## License

MIT
