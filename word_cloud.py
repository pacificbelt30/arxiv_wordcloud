import json
import requests
from wordcloud import WordCloud
from arxiv_api import ArXiv, SortBy, SortOrder


# WordCloudを作成して，Discordに通知するクラス
class Webhook():
    def __init__(self, query_txt, filename='wordcloud.png'):
        self.url = '' # クエリを行うWebhookのURL
        try:
            with open('.env', 'r') as f:
                url = json.load(f)['url']
                print('url:', url)
                self.url = url
        except:
            import traceback
            traceback.print_exc()

        self.filename = filename # WordCloudの保存先
        self.query_txt = query_txt # クエリテキスト

    # arXivにクエリを行い，WordCloudを作成
    def create_wordcloud(self):
        wordcloud = WordCloud(width=400, height=400, scale=1, max_words=200, min_font_size=4, min_word_length=1)
        arxiv = ArXiv()
        arxiv.query(query_txt)

        # WordCloud作成
        wordcloud.generate(' '.join(arxiv.titles))
        wordcloud.to_file(self.filename)
        return

    # Discordへ通知を行う
    def post_wordcloud_to_discord(self):
        contents = {
            'username' : 'arXiv WordCloud Notification',
            'image': self.filename
        }

        requests.post(self.url, json=contents)
        return

if __name__ == "__main__":
    query_txt = 'Watermark'

    wh = Webhook(query_txt)
    wh.create_wordcloud()
    wh.post_wordcloud_to_discord()
