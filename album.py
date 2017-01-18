import argparse
import json
import os

import requests
from requests.exceptions import RequestException

from .kagetora import Kagetora


class AlbumDownloader(Kagetora):
    def __init__(self, setting):
        super().__init__(setting)
        self.urls = []

    def search(self, word):
        self.driver.get('http://kagetora.bushidoo.com/album')
        self.find('.search-form input[name="qs"]').send_keys(word)
        self.find('.search-form').submit()

    def fetch_image_urls(self):
        page_count = len(self.finds('.pagination li'))

        self.urls = []
        for page in range(1, page_count + 1):
            self.find('.pagination a[data-page="{}"]'.format(page)).click()
            self.driver.refresh()  # to handle StaleElementReferenceException
            print(self.driver.current_url)

            thumbs = self.finds('.thumbnail img')
            self.urls += [t.get_property('src').replace('thumb', 'photo') for t
                          in thumbs]

    def download(self, dirname):
        os.makedirs(dirname, exist_ok=True)
        session = requests.Session()
        cookies = self.driver.get_cookies()

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        for i, url in enumerate(self.urls):
            try:
                request = session.get(url)
                with open(os.path.join(dirname, os.path.basename(url) + '.jpg'),
                          'wb') as f:
                    f.write(request.content)
                print('{}/{} {}'.format(i + 1, len(self.urls), url))
            except RequestException:
                print('[Error] {}'.format(url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kagetora Image Downloader')
    parser.add_argument('word', metavar='WORD', type=str, help='search word')
    parser.add_argument('-s', '--setting', default='setting.json', type=str,
                        metavar='',
                        help='Setting file name (default: setting.json)')
    args = parser.parse_args()

    with open(args.setting, 'r') as f:
        setting = json.load(f)

    d = AlbumDownloader(setting)
    d.search(args.word)
    d.fetch_image_urls()
    d.download(args.word)
    d.driver.quit()
