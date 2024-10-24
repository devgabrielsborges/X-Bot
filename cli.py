from xbot_class import Xbot


if __name__ == '__main__':
    # Getting a product from the database
    xbot = Xbot(int(input('Enter the index: ')))
    print(xbot.item.list_info())   # ['product', 'value', 'last_value', 'link']
    print(xbot.set_tweet_body())
