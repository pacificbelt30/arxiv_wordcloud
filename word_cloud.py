from wordcloud import WordCloud
from arxiv_api import ArXiv

base = "http://export.arxiv.org/api/query"
cat = "cs.AI"
start = 0
max_results = 20
sort_by = 'lastUpdatedDate'
sort_order = 'descending'

query_txt = 'Watermark'

wordcloud = WordCloud(width=400, height=400, scale=1, max_words=200, min_font_size=4, min_word_length=1)
arxiv = ArXiv(base, cat, start, max_results, sort_by, sort_order)
arxiv.query(query_txt)
wordcloud.generate(' '.join(arxiv.titles))
wordcloud.to_file('test.png')

webhook()
