# -*- coding:utf-8 -*-

"""
Main Part of Crawler
"""

import os
import re
import json
import time
from twitter import oauth_dance, read_token_file
from crawl_functions import streaming_filter_search
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

    dir_name = "baseball"
    filter_words = "ホークス,日ハム,西武,ロッテ,楽天,オリックス,巨人,阪神,カープ,ベイスターズ,中日,ヤクルト"
    # filter_words = "AKB"
    if not os.path.isdir('./data/' + dir_name):
        os.mkdir('./data/' + dir_name)

    tweets = []
    text_set = set()
    text_num = "0"

    # tweet search
    tweet = streaming_filter_search(words=filter_words, oauth_key_dict=oath_key_dict)
    for t in tweet.iter_lines():
        stream = t.decode("utf-8")
        try:
            find = json.loads(stream)
            print(find['text'])
        except json.decoder.JSONDecodeError:
            pass

    # 実行時間の表示
    elapsed_time = time.time() - start
    print(("実行時間:{0}".format(elapsed_time)) + "[sec]")


if __name__ == "__main__":
    main()