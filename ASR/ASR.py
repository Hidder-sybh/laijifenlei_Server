# coding=UTF-8
import re
import jieba
import json
from db_operator.item_db import ItemDb


def DelNoneWord(text: str):
    none_use_word = []
    with open('cfg/none_use_word.json', encoding='utf-8') as f:
        none_use_word = json.load(f)
    for now_key in none_use_word:
        text = text.replace(now_key, '')
    return text


def get_key(text: str):
    text_group = jieba.lcut(DelNoneWord(text))
    result = []
    for str in text_group:
        if str != '垃圾':
            result.append(str)
    return result


def ASR(text):
    key_group = get_key(text)
    result = {}
    item_message = ItemDb()
    for key in key_group:
        search_results = item_message.item_search_exact(key)
        if len(search_results) == 0:
            search_results = item_message.items_search_vague(key)
        result[key] = search_results
    item_message.close()
    return result
