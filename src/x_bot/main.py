"""
Runs the automation. First, retrieve the current index for the post,
using this index to search for the product in the spreadsheet.
Then, based on the product information, establish a chat in
Groq Cloud with the chosen specifications From there, the model
generates a message for the tweet to be posted, and the tweet is then
posted Finally, the bot prepares to send an SMS to the phone number you have
registered with Twilio, containing a customizable message
"""

from .xbot_class import Xbot


def main():
    xbot = Xbot()
    xbot.set_tweet_body()
    xbot.post_tweet()


if __name__ == "__main__":
    main()
