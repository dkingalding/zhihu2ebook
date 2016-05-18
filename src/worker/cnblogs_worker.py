#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup

from src.tools.http import Http
from src.tools.match import Match
from src.worker.page_worker import PageWorker

from src.lib.parser_tools import ParserTools
from src.lib.cnblogs_parser.author import CnblogsAuthorParser


class CnblogsAuthorWorker(PageWorker):
    u"""
    cnblogs author worker
    """
    @staticmethod
    def parse_max_page(content):
        match_object = re.search(r'共(?P<page_num>[^/\n\r]*)页', content)
        if match_object is not None:
            page_num = match_object.group('page_num')
        else:
            page_num = 1
        return page_num

    def catch_info(self, target_url):
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = CnblogsAuthorParser(content)
        self.info_list.append(parser.get_extra_info())
        print u"info_list???" + str(self.info_list)
        return

    def create_save_config(self):
        config = {
            'cnblogs_article': self.answer_list,
            'cnblogs_info': self.info_list
        }
        return config

    def parse_content(self, content):
        parser = CnblogsAuthorParser(content)
        self.answer_list += parser.get_answer_list()

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return

        self.task_complete_set.add(target_url)
        print u"target_url" + str(target_url)
        url = target_url + '?page=2'      # there are page num in this url

        content = Http.get_content(url)
        page_num = self.parse_max_page(content)

        print u"page_num???" + str(page_num)
        for item in range(int(page_num)):
            url = target_url + '?page={}'.format(str(item+1))
            print u"wtf url???" + str(url)
            content = Http.get_content(url)
            parser = CnblogsAuthorParser(content)
            article_url_list = parser.get_article_list()
            print "article_url_list???" + str(article_url_list)
            for item in article_url_list:
                self.work_set.add(item)
        return

