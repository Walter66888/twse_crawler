# linebot_handler/callback.py
import os
import datetime
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from database.mongodb import get_latest_data
from crawler.twse_crawler import parse_table_text, fetch_twse_data

# 讀取 LINE Channel 設定值
line_channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
line_channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    LINE Bot 處理用戶文字訊息：
      - 從資料庫取得最新資料，若資料不存在則嘗試即時爬取一次
      - 根據資料日期判斷是否為今日資料，並回覆提示訊息
    """
    latest_data = get_latest_data()
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    if not latest_data:
        # 第一次執行時資料庫無資料，嘗試直接爬取一次
        data = fetch_twse_data()
        if data:
            from database.mongodb import update_data
            update_data(data)
            latest_data = data
        else:
            reply_text = "目前資料尚未產生，請稍後再試。"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

    table_text = parse_table_text(latest_data["content"])
    if latest_data["date"] != today_str:
        reply_text = f"【提醒】今日資料尚未更新，以下提供前一日資料（{latest_data['date']}）：\n{table_text}"
    else:
        reply_text = f"【最新資料】（{latest_data['date']}）：\n{table_text}"
    try:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    except Exception as e:
        print("LINE 回覆錯誤：", e)

def callback_route():
    """
    Flask Webhook 路由處理，用來接收 LINE 發送的訊息。
    """
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"
