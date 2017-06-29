# -*- coding:utf-8 -*-

"""
Main Part of Crawler
"""

import os
import re
import time
from twitter import oauth_dance, read_token_file
from crawl_functions import timeline_search
from local_info import API_key, API_secret

# get accessToken and accessSecret
MY_TWITTER_CREDS = os.path.expanduser(r'.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("100m_tweet_crawler", API_key, API_secret, MY_TWITTER_CREDS)
oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

oath_key_dict = {
    "consumer_key": API_key,
    "consumer_secret": API_secret,
    "access_token": oauth_token,
    "access_token_secret": oauth_secret
}


def main():
    # 実行時間の計算
    start = time.time()

    # screen_name = "positive_bot3"
    # screen_name = "kami_positive"
    screen_name = "ureshinokouji"
    if not os.path.isdir('./data/' + screen_name):
        os.mkdir('./data/' + screen_name)
    tweets = []
    text_set = set()
    max_id = None
    text_num = "0"

    t0 = time.time()
    for index in range(10):

        # tweet search
        tweet_list = timeline_search(screen_name=screen_name,
                                     max_id=max_id,
                                     oauth_key_dict=oath_key_dict)
        time.sleep(5)                                                              # interval

        # if a crawler success to crawl twitter data...
        if tweet_list is not None:

            # cleaning text data
            for post in tweet_list:
                post['text'] = re.sub(r'\n', r" ", post['text'])
                post['text'] = re.sub(r'\r\n', r" ", post['text'])
                post['text'] = re.sub(r'@(\w+)', r" ", post['text'])
                tweets.append(post)

            # collect next max_id
            max_id = tweet_list[-1]['id']

        # save as text
        with open("data/" + screen_name + "/data_" + text_num + ".txt", "a", encoding="utf-8") as f1:
            for tweet in tweets:
                if len(tweet['entities']['urls']) == 0:                        # remove tweets including URL
                    if tweet['text'] not in text_set:                          # remove same tweets
                        f1.write(tweet['text'] + "\n")
                        text_set.add(tweet['text'])
        tweets.clear()

        # rename text
        text_num = str(index + 1)

        # time restricted
        if (index + 1) % 90 == 0:
            t1 = time.time()
            if (900 - (t1 - t0)) > 0:
                print(900 - (t1 - t0), "[sec] time sleep for the next tweet crawl")
                time.sleep(900 - (t1 - t0))
            t0 = time.time()

        print(index + 1, "crawl end")

    # 実行時間の表示
    elapsed_time = time.time() - start
    print(("実行時間:{0}".format(elapsed_time)) + "[sec]")


if __name__ == "__main__":
    main()