#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


class Match(object):
    # zhihu
    @staticmethod
    def xsrf(content=''):
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content)
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''

    @staticmethod
    def answer(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})/answer/(?P<answer_id>\d{8})', content)

    @staticmethod
    def question(content=''):
        return re.search(r'(?<=zhihu\.com/)question/(?P<question_id>\d{8})', content)

    @staticmethod
    def author(content=''):
        return re.search(r'(?<=zhihu\.com/)people/(?P<author_id>[^/\n\r]*)', content)

    @staticmethod
    def collection(content=''):
        return re.search(r'(?<=zhihu\.com/)collection/(?P<collection_id>\d*)', content)

    @staticmethod
    def topic(content=''):
        return re.search(r'(?<=zhihu\.com/)topic/(?P<topic_id>\d*)', content)

    @staticmethod
    def article(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/]*)/(?P<article_id>\d{8})', content)

    @staticmethod
    def column(content=''):
        return re.search(r'(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)', content)

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)

def get_url_type(url):
    type_regex_dict = {
        "question": "(?<=zhihu\.com/)question/(?P<question_id>\d{8})",
        "column": "(?<=zhuanlan\.zhihu\.com/)(?P<column_id>[^/\n\r]*)",
    }
    for k, v in type_regex_dict.items():
        search_result = re.search(v, url)
        if search_result is not None:
            return k
    return 'unknown'