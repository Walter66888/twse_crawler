# database/__init__.py
# 將 mongodb 模組中的主要函式匯出，方便外部直接從 database 匯入操作資料庫的方法
from .mongodb import update_data, get_latest_data
