# database/mongodb.py
import os
from pymongo import MongoClient

# 從環境變數讀取 MongoDB 連線字串
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["twstock"]
collection = db["chip_data"]

def update_data(data):
    """
    根據日期（字串型式）更新或插入資料，若資料已存在則更新，否則新增。
    """
    if data is None:
        return
    collection.update_one(
        {"date": data["date"]},
        {"$set": data},
        upsert=True
    )
    print(f"存入資料日期 {data['date']} 成功")

def get_latest_data():
    """
    依據日期排序取得最新一筆資料。
    """
    return collection.find_one(sort=[("date", -1)])
