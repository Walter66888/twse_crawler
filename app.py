# app.py
import os
from flask import Flask
from linebot_handler.callback import callback_route
from scheduler.job_scheduler import start_scheduler

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    return callback_route()

if __name__ == "__main__":
    # 啟動定時任務
    start_scheduler()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
