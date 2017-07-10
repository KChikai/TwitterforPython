# -*- coding:utf-8 -*-

"""
データ整形用
"""

import re


def clean_pos(screen_name):
    """
    positive名言集の人名を除去する関数
    """
    pattern = r"(～|~)(.+?)(～\n|~\n|\n)"
    r = re.compile(pattern)

    with open("data/" + screen_name + "/data_clean_all.txt", "w", encoding="utf-8") as f:
        for line in open("data/" + screen_name + "/data_all.txt", "r", encoding="utf-8"):
            # m = r.search(line)
            # if m is not None:
            #     print(m, line)
            clean_text = re.sub(pattern, "\n", line)
            f.write(clean_text)


def clean_kami_pos(screen_name):
    """
    urlを除去する関数
    """
    pattern = r"(https:|http:)(.+?)(\n)"
    r = re.compile(pattern)

    with open("data/" + screen_name + "/data_clean_all.txt", "w", encoding="utf-8") as f:
        for line in open("data/" + screen_name + "/data_all.txt", "r", encoding="utf-8"):
            m = r.search(line)
            if m is not None:
                print(m, line)
            clean_text = re.sub(pattern, "\n", line)
            f.write(clean_text)


def main():
    # clean_pos(screen_name="positive_bot3")
    clean_kami_pos(screen_name="ureshinokouji")

if __name__ == '__main__':
    main()