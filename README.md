# kagetora scraper

景虎からいろいろ取ってきます。
サーバーに負担かかる気がするので使うのはほどほどにしましょう。

## Dependency

- Python 3.5.2 (3.5.1+)
- selenium 3.0.2 (`pip install -U selenium`)
- PhantomJS (`brew install phantomjs`)

Mac以外での動作確認はしていません。

## Getting Started

同じフォルダに景虎のログイン情報を書いた`setting.json`を作ります。

```json
{
    "shared_password": "共通パスワード",
    "user_initial": "○行",
    "user_name": "名字名前",
    "user_password": "個人パスワード"
}
```

## Usage

### アルバム検索して一括ダウンロードする

```bash
$ python album.py <word>
```

