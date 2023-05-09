import requests
import feedparser
import json

""" References
https://info.arxiv.org/help/api/user-manual.html
https://github.com/amueller/word_cloud
"""
"""
search_query: string
id_list: comma-delimited string
start: int
max_results: int
sortBy: 'relevance' | 'lastUpdatedDate' | 'submittedDate'
sortOrder: 'ascending' | 'descending'
"""

base = "http://export.arxiv.org/api/query"
cat = "cs.AI"
start = 0
max_results = 2
sort_by = 'lastUpdatedDate'
sort_order = 'descending'

# Return Atom 1.0 format
class ArXiv():
    def __init__(self, base:str, cat:str, start:int, max_results:int, sort_by, sort_order):
        self.base_url = base
        self.cat = cat
        self.start = start
        self.max_results = max_results
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.query_txt = ''
    
    @property
    def query_url(self):
        return f'{self.base_url}?search_query=cat:{self.cat}{"+AND+all:"+self.query_txt if not self.query_txt == "" else ""}&start={self.start}&max_results={self.max_results}&sortBy={self.sort_by}&sortOrder={self.sort_order}'

    @property
    def titles(self):
        return [paper['title'] for paper in self.response_dict['entries']]

    @property
    def summaries(self):
        return [paper['summary'] for paper in self.response_dict['entries']]

    @property
    def title_and_summary(self):
        return [t+s for t, s in zip(self.titles, self.summaries)]

    def query(self, query_txt):
        self.query_txt = query_txt if not query_txt == '' else self.query_txt
        print(self.query_url)
        self.response = requests.get(self.query_url)
        self.response_dict = feedparser.parse(self.response.text)

    def test(self):
        pass


if __name__ == "__main__":
    query_txt = ''
    a = ArXiv(base, cat, start, max_results, sort_by, sort_order)
    a.query(query_txt)

    print(a.response)
    print(json.dumps(feedparser.parse(a.response.text), indent=2))