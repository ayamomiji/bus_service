Bus Service
===========

## Setup

    pip install -r requirement
    ./manage.py migrate
    cp .env.example .env
    # 接著, 在 .env 填入必要資訊...

    # 啟動 django server 與 celery
    foreman start -f Procfile.dev

### 測試用 SMTP 架設

    python -m pip install aiosmtpd
    python -m aiosmtpd -n -l localhost:8025

## Usage

訂閱一個通知:

    curl -X POST 'http://localhost:8000/bus_notifiers/' -d '{
        "route": "307",
        "stop": "捷運南京復興站",
        "direction": 0,
        "email": "ayaya.zhao@gmail.com"
    }'

查詢所有訂閱項目:

    curl 'http://localhost:8000/bus_notifiers/'

得到 notifier id 後, 可以取消通知:

    curl -X DELETE 'http://localhost:8000/bus_notifiers/1'
