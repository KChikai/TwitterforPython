# -*- coding:utf-8 -*-

"""
Main Part of Crawler
"""

import os
import time
from twitter import oauth_dance, read_token_file, TwitterStream, OAuth, Twitter
from local_info import API_key, API_secret

# get accessToken and accessSecret
MY_TWITTER_CREDS = os.path.expanduser(r'.my_app_credentials')
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("100m_tweet_crawler", API_key, API_secret, MY_TWITTER_CREDS)
oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)


twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, API_key, API_secret))
stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, API_key, API_secret), secure=True)

# NG words
check_chara = ('http', '#', '\\', '【', '】')


def trim(text):
    """ 改行を適当に置き換える """
    return text.replace('\r', ' ').replace('\n', ' ')


def check(text):
    """ 禁止文字のチェックを行う """
    for char in check_chara:
        if char in text:
            return False
    return True


def search(tweet):
    """ in_reply_to_status_idから宛先となるツイートを参照する """

    retry_max = 5      # Retry MAX
    retry_time = 5     # Retry time

    for r in range(retry_max):

        # 言語が日本語、in_reply_to_status_idが明示されており、禁止単語を含まないツイートの場合
        if 'lang' in tweet and tweet['lang'] == 'ja' \
                and 'in_reply_to_status_id' in tweet and not tweet['in_reply_to_status_id'] is None \
                and 'text' in tweet and check(tweet['text']):

            # retrieve the response
            try:
                status = twitter.statuses.show(id=tweet['in_reply_to_status_id'])
            except:
                time.sleep(retry_time)
                continue
            if 'lang' in tweet and tweet['lang'] == 'ja' and 'text' in status and check(status['text']):
                save_text = trim(status['text']) + '\t' + trim(tweet['text']) + '\n'
                print(save_text, end='\n\n')
                return save_text
                # if 'in_reply_to_status_id' in status and not status['in_reply_to_status_id'] is None:
                #     search(status)
            else:
                print('bad post: ', status['text'], end='\n\n')
                break
        else:
            print('bad comment: ', tweet['text'], end='\n\n')
            break

    return None


def main():

    dir_name = "baseball"
    filter_words = "ホークス,日ハム,西武,ロッテ,楽天,オリックス,巨人,阪神,カープ,ベイスターズ,中日,ヤクルト"
    # filter_words = "AKB"
    if not os.path.isdir('./data/' + dir_name):
        os.mkdir('./data/' + dir_name)

    text_num = 0
    crawl_num = 0

    tweets_iter = stream.statuses.filter(track=filter_words)

    for tweet in tweets_iter:

        # search response
        text = search(tweet)

        # save as text
        if text is not None:
            with open("data/" + dir_name + "/data_" + str(text_num) + ".txt", "a", encoding="utf-8") as f1:
                f1.write(text)
                crawl_num += 1

        # rename file name
        if crawl_num != 0 and crawl_num % 10000 == 0:
            text_num += 1


if __name__ == "__main__":
    main()