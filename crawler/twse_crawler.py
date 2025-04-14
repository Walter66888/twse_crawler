# crawler/twse_crawler.py
import re
import datetime
import requests
from bs4 import BeautifulSoup

def fetch_twse_data():
    """
    爬取台灣證交所網站資料，解析頁面中的日期資訊，並將資料與爬取時間一併回傳。
    """
    url = "https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?response=html"
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
    except Exception as e:
        print("Error fetching TWSE data:", e)
        return None

    if response.status_code != 200:
        print("TWSE request 非 200 回應，狀態碼：", response.status_code)
        return None

    html = response.text

    # 使用正則表達式找出格式為 YYYY/MM/DD 的日期
    m = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', html)
    if m:
        data_date = f"{m.group(1)}{int(m.group(2)):02d}{int(m.group(3)):02d}"
    else:
        # 若解析失敗則預設為當天日期
        data_date = datetime.datetime.now().strftime("%Y%m%d")
    data = {
        "date": data_date,
        "content": html,
        "timestamp": datetime.datetime.now()
    }
    return data

def parse_table_text(html):
    """
    解析 HTML 表格內容，轉換為純文字格式，方便回覆用戶。
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    if not table:
        return "無法解析資料表格"
    rows = table.find_all("tr")
    text_lines = []
    for row in rows:
        cols = row.find_all(["th", "td"])
        cols_text = [col.get_text(strip=True) for col in cols]
        text_lines.append(" | ".join(cols_text))
    return "\n".join(text_lines)
