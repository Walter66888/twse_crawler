# crawler/__init__.py
# 將 twse_crawler 模組中的函式匯出，方便外部直接從 crawler 匯入相關功能
from .twse_crawler import fetch_twse_data, parse_table_text
