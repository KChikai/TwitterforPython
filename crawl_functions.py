# -*- coding:utf-8 -*-

"""
データ取得用関数群
"""

from requests_oauthlib import OAuth1Session
import json
import time
from requests.exceptions import ConnectionError


def create_oath_session(oauth_key_dict):
    oath = OAuth1Session(
        oauth_key_dict["consumer_key"],
        oauth_key_dict["consumer_secret"],
        oauth_key_dict["access_token"],
        oauth_key_dict["access_token_secret"]
    )
    return oath


def timeline_search(screen_name, max_id, oauth_key_dict):
    """
    特定ユーザのタイムラインからツイートを取得
    :param screen_name: 取得したいユーザのスクリーンネーム
    :param max_id: 欲しいツイート群の時系列的に一つ上のツイートID（このツイートはクロール対象外）
    :param oauth_key_dict: アクセスキー
    :return: 200件のツイートデータリスト (ref: https://syncer.jp/Web/API/Twitter/REST_API/GET/statuses/user_timeline/)
    """
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

    oath = create_oath_session(oauth_key_dict)
    try:
        responses = oath.get(url, params=params)
    except ConnectionError:
        time.sleep(180)
        responses = oath.get(url, params=params)
    if responses.status_code != 200:
        print("Error code: %d " % responses.status_code, "ID:", screen_name)
        return None
    else:
        tweet_list = json.loads(responses.text)
        return tweet_list

