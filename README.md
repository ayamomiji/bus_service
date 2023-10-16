Bus Service
===========

## Setup

    pip install -r requirement
    ./manage.py migrate
    cp .env.example .env
    # 接著, 在 .env 填入必要資訊...
    ./manage.py downloaddata # 下載公車資料
    foreman start -f Procfile.dev # 啟動 django server 與 celery

## Usage

查詢路線與經過站牌的 id:

    curl 'http://localhost:8000/bus_data/routes?q=307' | jq

訂閱一個通知:

    curl -X POST 'http://localhost:8000/bus_notifiers/' -d '{
        "route_id": 613,
        "stop_id": 22961
    }'

查詢所有訂閱項目:

    curl 'http://localhost:8000/bus_notifiers/'

得到 notifier id 後, 可以取消通知:

    curl -X DELETE 'http://localhost:8000/bus_notifiers/3'
