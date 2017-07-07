# -*- coding: utf-8 -*-
import sys
import fasttext as ft
import subprocess as cmd

obj = sys.argv[1]
morp = cmd.getstatusoutput("echo " + obj + " | mecab -Owakati")
words = morp[1]
print('\n', words)

classifier = ft.load_model('data/new.bin')
estimate = classifier.predict([words], k=2)
estimate_2 = classifier.predict_proba([words], k=2)
print(estimate[0])
if estimate[0][0] == "__label__1,":
    print('ネガティブ', estimate_2[0][0][1])
elif estimate[0][0] == "__label__2,":
    print('ポジティブ', estimate_2[0][0][1])