import requests
from bs4 import BeautifulSoup
import time

# 掲示板のURLとDiscord WebhookのURLを設定
URL = "http://smalog.jp/thread.php?id=himitsu&no=26711&rid=8787&guid=on&PHPSESSID=aef3dda2e389ac581eaedb75cabf5225"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1347504160513327194/VKkkRuSCLKyQDY4kGDnAovBupp7pw8CcA7IuVbpeBYQ-euwgC3ep808mmgZP1TgC0D5F"

def get_latest_posts():
    """掲示板の最新投稿一覧を取得"""
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 投稿のリンク（ID）を取得
    posts = soup.find_all("a", class_="mini-button")

    # 各投稿のIDを取得
    extracted_posts = []
    for post in posts:
        post_id = post.text.strip()  # 投稿IDを取得
        extracted_posts.append(post_id)

    print(f"🔍 取得した投稿の数: {len(extracted_posts)}")
    for idx, post_id in enumerate(extracted_posts):
        print(f"投稿 {idx + 1}: ID={post_id}")

    return extracted_posts

def send_to_discord(message):
    """Discord に通知を送る"""
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ Discord 通知送信成功")
    else:
        print(f"⚠️ Discord 通知送信失敗: {response.status_code}")

if __name__ == "__main__":
    latest_posts = get_latest_posts()  # 初回取得
    print(f"📝 初回の latest_posts: {latest_posts}")

    while True:
        print("\n🔍 掲示板をチェック中...")

        new_posts = get_latest_posts()

        # 新しく追加された投稿を特定
        added_posts = [post for post in new_posts if post not in latest_posts]

        if added_posts:
            for new_post in added_posts:
                print(f"📢 新しい投稿を検出: ID={new_post}")
                send_to_discord(f"📢 みいから新しい投稿があります！\n投稿ID: {new_post}")
            latest_posts = new_posts  # **最新の投稿リストを更新**
        else:
            print("💤 新しい投稿はありません")

        print(f"📝 現在の latest_posts: {latest_posts}")  # 確認用ログ
        time.sleep(10)  # 10秒ごとにチェック
