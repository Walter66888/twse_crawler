import multiprocessing

bind = "0.0.0.0:5000"  # 可根據 Render 指定的 PORT 調整或使用環境變數
workers = multiprocessing.cpu_count() * 2 + 1  # 自動根據 CPU 數量計算 worker 數量
timeout = 120  # 請求超時時間

def on_starting(server):
    # 此函式在 master process 啟動時執行一次
    # 啟動 APScheduler 排程任務
    from scheduler.job_scheduler import start_scheduler
    start_scheduler()
    print("Scheduler 已由 gunicorn master process 啟動")
