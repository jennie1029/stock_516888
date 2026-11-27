
# 先導入會用到的套件
import requests
from bs4 import BeautifulSoup
import time
import os

# 要查詢的股票
stock = ["7967", "2344", "009827"]

# Telegram Bot 設定
# 建議將 Token 和 Chat ID 設定在 GitHub Secrets
token = os.getenv("9191219101:AAGFd1DStUt_4yydLyd8JLbI-VWhsjAY9M4")
chat_id = os.getenv("9027536949")

# 檢查 Telegram 設定
if not token or not chat_id:
    raise ValueError("請設定 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

# 建立 HTTP 請求標頭
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 依序查詢股票
for stockid in stock:

    try:
        print(f"正在查詢股票：{stockid}")

        # 組合 Yahoo 股市網址
        url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"

        # 發送請求
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 尋找股價元素
        price = None

        for span in soup.find_all("span"):
            classes = span.get("class", [])

            if "Fz(32px)" in classes and "Fw(b)" in classes:
                text = span.get_text(strip=True)

                if text:
                    price = text
                    break

        # 找不到股價時
        if not price:
            print(f"股票 {stockid} 找不到股價")
            continue

        # 組合 Telegram 訊息
        message = f"股票 {stockid} 即時股價為 {price}"

        print(message)

        # 發送 Telegram 訊息
        telegram_url = (
            f"https://api.telegram.org/bot{token}/sendMessage"
        )

        telegram_response = requests.post(
            telegram_url,
            data={
                "chat_id": chat_id,
                "text": message
            },
            timeout=15
        )

        telegram_response.raise_for_status()

        result = telegram_response.json()

        if not result.get("ok"):
            print(f"Telegram 發送失敗：{result}")
        
        # 每次查詢間隔 3 秒
        time.sleep(3)

    except requests.RequestException as e:
        print(f"股票 {stockid} 網路請求錯誤：{e}")
        continue

    except Exception as e:
        print(f"股票 {stockid} 發生錯誤：{e}")
        continue

print("所有股票查詢完成！")
