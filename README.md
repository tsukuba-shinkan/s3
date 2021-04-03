# S3

Sloppy Shinkan Search

# 使い方

```
docker pull yukijs/shinkan-s3
docker run -p 80:8000 --restart=always -d --name s3 yukijs/shinkan-s3
```

# エンドポイント

団体検索　/search/org?q=キーワード
イベント検索　/search/events?q=キーワード&rangestart=2021-04-10&rangeend=2021-04-10
ランダムの表示　/random/org?n=15
ワードプレスと同期(これ叩きまくったやつ、IP 集めて警察へ投げる)　/sync
全ての団体を取得　/all
