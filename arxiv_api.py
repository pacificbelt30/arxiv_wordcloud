import requests
import re
import feedparser
import json
import pandas as pd
from enum import Enum
from typing import List

""" References
https://info.arxiv.org/help/api/user-manual.html
https://github.com/amueller/word_cloud
"""


# どの要素でソートするか
class SortBy(Enum):
    relevance = 'relevance'
    lastUpdatedDate = 'lastUpdatedDate'
    submittedDate = 'submittedDate'


# 昇順 or 降順
class SortOrder(Enum):
    ascending = 'ascending'
    descending = 'descending'


"""
search_query: string
id_list: comma-delimited string
start: int
max_results: int
sortBy: 'relevance' | 'lastUpdatedDate' | 'submittedDate'
sortOrder: 'ascending' | 'descending'
"""
class ArXiv():
    def __init__(self, base:str='http://export.arxiv.org/api/query', cat:str='cs.AI', start:int=0, max_results:int=20, sort_by:SortBy=SortBy.lastUpdatedDate, sort_order:SortOrder=SortOrder.descending):
        self.base_url = base
        self.cat = cat
        self.start = start
        self.max_results = max_results
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.query_txt = ''
    
    @property
    def query_url(self) -> str:
        return f'{self.base_url}?search_query=cat:{self.cat}{"+AND+all:"+self.query_txt if not self.query_txt == "" else ""}&start={self.start}&max_results={self.max_results}&sortBy={self.sort_by.value}&sortOrder={self.sort_order.value}'

    @property
    def titles(self) -> List[str]:
        return [paper['title'] for paper in self.response_dict['entries']]

    @property
    def urls(self) -> List[str]:
        return [paper['url'] for paper in self.response_dict['entries']]

    @property
    def summaries(self) -> List[str]:
        return [paper['summary'] for paper in self.response_dict['entries']]

    @property
    def title_and_summary(self) -> List[str]:
        return [t+s for t, s in zip(self.titles, self.summaries)]

    # これは使えない
    def get_table(self):
        all_txt = ''
        for txt in self.title_and_summary:
            all_txt += txt
        unique_word_list = list(set(re.split('[ ,.\n]', re.sub('\d+', '', re.sub('[^ ,.\n]{0,2}', '', all_txt)))))[1:]
        print(unique_word_list)
        # unique_word_listの引数を取る

        # 各論文に対してその単語があるかどうかのベクトルを作成
        table = []
        for i in range(len(self.titles)):
            table.append([])
            for j in range(len(unique_word_list)):
                table[i].append(1 if (unique_word_list[j] in self.title_and_summary[i]) else 0)

        df = pd.DataFrame(data=table,index=self.titles, columns=unique_word_list)
        print(df)
        print(df.sum('index').sort_values())

    # arXiv APIへのクエリ
    # response Atom 1.0 format
    def query(self, query_txt):
        self.query_txt = query_txt if not query_txt == '' else self.query_txt
        self.response = requests.get(self.query_url)
        self.response_dict = feedparser.parse(self.response.text)
        return


if __name__ == "__main__":
    base = "http://export.arxiv.org/api/query"
    cat = "cs.AI"
    start = 0
    max_results = 10
    sort_by = SortBy.lastUpdatedDate
    sort_order = SortOrder.descending

    query_txt = ''
    arxiv = ArXiv(base, cat, start, max_results, sort_by, sort_order)
    arxiv.query(query_txt)

    arxiv.get_table()
