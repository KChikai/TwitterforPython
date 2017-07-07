# -*- coding:utf-8 -*-

"""
データ取得用関数群
"""

from requests_oauthlib import OAuth1Session, OAuth1
import json
import time
import requests
from requests.exceptions import ConnectionError


def create_oath_session(oauth_key_dict):
    oath = OAuth1Session(
        oauth_key_dict["consumer_key"],
        oauth_key_dict["consumer_secret"],
        oauth_key_dict["access_token"],
        oauth_key_dict["access_token_secret"]
    )
    return oath


def create_oath_object(oauth_key_dict):
    auth = OAuth1(
        oauth_key_dict["consumer_key"],
        oauth_key_dict["consumer_secret"],
        oauth_key_dict["access_token"],
        oauth_key_dict["access_token_secret"]
    )
    return auth


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


def streaming_filter_search(words, oauth_key_dict):
    """
    Streaming API から filter したツイートを取得 (試作品)
    :param words: filterにかけたいキーワード（カンマ区切りはOR，スペース区切りはAND）
    :param oauth_key_dict: アクセスキー
    :return:
    """

    # set parameters
    url = "https://stream.twitter.com/1.1/statuses/filter.json?"
    params = {
        "language": "ja",
        "track": words,
    }
    auth = create_oath_object(oauth_key_dict)

    # get request
    try:
        responses = requests.post(url, auth=auth, stream=True, data=params)
    except ConnectionError:
        time.sleep(180)
        responses = requests.get(url, auth=auth, stream=True, data=params)

    # convert json data
    if responses.status_code != 200:
        print("Error code: %d " % responses.status_code, "ID:", words)
        return None
    else:
        print('success to crawl twitter data')
        return responses

