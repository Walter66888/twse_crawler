# scheduler/job_scheduler.py
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from crawler.twse_crawler import fetch_twse_data
from database.mongodb import update_data

def job_fetch():
    """
    定時任務：每天14:50開始爬取 TWSE 資料，判斷是否為當日更新，並存入資料庫。
    """
    print("啟動定時爬蟲任務：", datetime.datetime.now())
    data = fetch_twse_data()
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    if data:
        if data["date"] == today_str:
            print("今日資料已更新")
        else:
            print("今日資料尚未更新，抓取為前一日資料")
        update_data(data)
    else:
        print("爬取 TWSE 資料失敗")

def start_scheduler():
    """
    啟動 APScheduler，設定時區為 Asia/Taipei，並於每天14:50執行 job_fetch。
    """
    scheduler = BackgroundScheduler(timezone="Asia/Taipei")
    scheduler.add_job(job_fetch, 'cron', hour=14, minute=50)
    scheduler.start()
    print("APScheduler 已啟動")
