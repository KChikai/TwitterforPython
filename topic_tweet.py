#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import json
import time
import calendar
from requests_oauthlib import OAuth1Session
from twitter import oauth_dance, read_token_file
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


def create_oath_session(oathkeydict):
    oath = OAuth1Session(
        oathkeydict["consumer_key"],
        oathkeydict["consumer_secret"],
        oathkeydict["access_token"],
        oathkeydict["access_token_secret"]
    )
    return oath


def ymd_hms(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return time.strftime("%Y-%m-%d_%H:%M:%S_%Z", time_local)


def tweet_search(search_word, oathkeydict, max_id=None):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    if max_id is None:
        params = {
            "q": search_word,
            "result_type": "recent",
            "lang": "ja",
            "count": "1",
            }
    else:
        params = {
            "q": search_word,
            "result_type": "recent",
            "lang": "ja",
            "count": "100",
            "max_id": max_id - 1,
            }

    oath = create_oath_session(oathkeydict)

    try:
        response = oath.get(url, params=params)
    except ConnectionError:
        time.sleep(180)
        response = oath.get(url, params=params)

    if response.status_code != 200:
        print("Error code: ", response.status_code)
        return None
    tweets = json.loads(response.text)
    return tweets


def main():

    query = "#モンスト+OR+#smap+OR+#ももクロ+OR+#オリックス+OR+#ポケモンGO+OR+#carp+OR+#ミスコン+OR+#sbhawks"
    max_id = crawl_count = 0
    t0 = time.time()
    tweets = tweet_search(query, oath_key_dict)
    crawl_count += 1
    time.sleep(5)
    with open('./result.dat', 'a', encoding='utf-8') as f:
        while True:
            for tweet in tweets["statuses"]:
                if max_id > tweet["id"] or max_id == 0:
                    max_id = tweet["id"]
                text = re.sub(r'(\n|\r\n)', r"", tweet['text'])
                f.write(tweet["id_str"] + '\t' + text + '\n')

            if len(tweets) == 0:
                break

            tweets = tweet_search(query, oath_key_dict, max_id=max_id)
            crawl_count += 1
            time.sleep(5)

            # time restrict
            if crawl_count % 170 == 0 and crawl_count != 0:
                t1 = time.time()
                if (900 - (t1 - t0)) > 0:
                    print(900 - (t1 - t0), "[sec] time sleep for the next tweet crawl")
                    time.sleep(900 - (t1 - t0))
                t0 = time.time()

            # show log
            if crawl_count % 100 == 0:
                print("Crawl Count: ", crawl_count)

    # for i in range(1):
    #     tweets = tweet_search(query, oath_key_dict)
    #     for tweet in tweets["statuses"]:
    #         tweet_id = tweet[u'id_str']
    #         text = tweet[u'text']
    #         created_at = tweet[u'created_at']
    #         # user_id = tweet[u'user'][u'id_str']
    #         # user_description = tweet[u'user'][u'description']
    #         # screen_name = tweet[u'user'][u'screen_name']
    #         # user_name = tweet[u'user'][u'name']
    #         print("tweet_id:", tweet_id)
    #         print("text:", text)
    #         print("created_at:", created_at)
    #         print("created_at2:", ymd_hms(created_at))
    #         # print("user_id:", user_id)
    #         # print("user_desc:", user_description)
    #         # print("screen_name:", screen_name)
    #         # print("user_name:", user_name)
    #         print('')

if __name__ == "__main__":
    main()