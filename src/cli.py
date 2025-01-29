import sys
from .xbot_class import Xbot


def main():
    # Use the first CLI argument as an index if available, otherwise default to 0
    if len(sys.argv) > 1:
        index = int(sys.argv[1])
    else:
        return
    
    xbot = Xbot(index)
    print(xbot.item.list_info())   # ['product', 'value', 'last_value', 'link']
    print(xbot.set_tweet_body())

if __name__ == '__main__':
    main()