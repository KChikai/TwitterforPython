# -*- coding:utf-8 -*- #

from requests_oauthlib import OAuth1Session
import json
import os
import re
import time
from twitter import *
from requests.exceptions import ConnectionError
from local_info import API_key, API_secret

# accessTokenとaccessSecretの取得
MY_TWITTER_CREDS = os.path.expanduser(r'.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("100m_tweet_crawler", API_key, API_secret, MY_TWITTER_CREDS)
oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

t = Twitter(auth=OAuth(oauth_token, oauth_secret, API_key, API_secret))

oath_key_dict = {
    "consumer_key": API_key,
    "consumer_secret": API_secret,
    "access_token": oauth_token,
    "access_token_secret": oauth_secret
}


def create_oath_session(oathkeydict):
    oath = OAuth1Session(
        oathkeydict["consumer_key"],
        oathkeydict["consumer_secret"],
        oathkeydict["access_token"],
        oathkeydict["access_token_secret"]
    )
    return oath


def timeline_search(screen_name, max_id, oathkeydict):
    # if tweet_id is None:
    #     return None
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    if max_id is not None:
        params = {
            "screen_name": screen_name,
            "count": 200,
            "include_rts": False,
            "max_id": max_id,
        }
    else:
        params = {
            "screen_name": screen_name,
            "count": 200,
            "include_rts": False,
        }

    oath = create_oath_session(oathkeydict)
    try:
        responses = oath.get(url, params=params)
    except ConnectionError:
        time.sleep(60)
        responses = oath.get(url, params=params)
    if responses.status_code != 200:
        print("Error code: %d " % responses.status_code, "ID:", screen_name)
        return None
    else:
        tweet_list = json.loads(responses.text)
        return tweet_list


def main():
    # 実行時間の計算
    start = time.time()

    pos_tweets = []
    text_set = set()
    max_id = None
    text_num = "0"

    t0 = time.time()
    for index in range(10):

        # tweet search
        tweet_list = timeline_search(screen_name="positive_bot3", max_id=max_id, oathkeydict=oath_key_dict)
        time.sleep(5)               # interval

        # if a crawler success to crawl twitter data...
        if tweet_list is not None:

            # cleaning text data
            for p in tweet_list:
                p['text'] = re.sub(r'\n', r" ", p['text'])
                p['text'] = re.sub(r'\r\n', r" ", p['text'])
                p['text'] = re.sub(r'@(\w+)', r" ", p['text'])
                pos_tweets.append(p)
            # collect next max_id
            max_id = tweet_list[-1]['id']

        # save as text
        if (index + 1) % 1 == 0:
            with open("data/data_" + text_num + ".txt", "a", encoding="utf-8") as f1:
                for post_tweet in pos_tweets:
                    if len(post_tweet['entities']['urls']) == 0:                    # remove tweets including URL
                        if post_tweet['text'] not in text_set:                      # remove same tweets
                            f1.write(post_tweet['text'] + "\n")
                            text_set.add(post_tweet['text'])
            pos_tweets.clear()

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

    # to pass in the GET/POST parameter `id` you need to use `_id`
    # print(t.statuses.oembed(_id=418033807850496002))

    # 実行時間の表示
    elapsed_time = time.time() - start
    print(("実行時間:{0}".format(elapsed_time)) + "[sec]")


if __name__ == "__main__":
    main()