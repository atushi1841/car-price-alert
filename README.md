# Japan Car Price Alert

中古車（goo-net.com）の価格アラートサービス。

モデル名と希望価格上限を登録すると、毎日goo-netをクロールし、
希望価格以下の車両が見つかったらメールで通知する。

## 機能
- アラート登録（モデル名・上限価格・メール）
- 毎日自動クロール（goo-net全車をスキャンしモデル名でマッチ）
- 価格が閾値以下ならメール通知
- 全角/半角キーワード自動対応

## 起動
```bash
pip install -r requirements.txt
SMTP_HOST=smtp.example.com SMTP_USER=user SMTP_PASS=pass \
uvicorn app:app --host 0.0.0.0 --port 8000
```

SMTP未設定時は通知をログ出力（開発モード）。

## エンドポイント
- `GET /` — アラート登録フォーム
- `POST /alerts` — 登録
- `GET /alerts` — 登録済み一覧
- `POST /run-check` — 手動クロール（全アラートチェック）

## データ
SQLite（`alerts.db`）— アラート情報と最終チェック時刻のみ。

## Apify Store

- [japan-market-mcp](https://apify.com/store/actors/japan-market-mcp) — Apify Store actor (total runs: 604)
- [japan-offmall-market-scraper](https://apify.com/store/actors/japan-offmall-market-scraper) — Apify Store actor (total runs: 381)
- [mandarake-auction-scraper](https://apify.com/store/actors/mandarake-auction-scraper) — Apify Store actor (total runs: 358)
- [tackleberry-japan-fishing-tackle-scraper](https://apify.com/store/actors/tackleberry-japan-fishing-tackle-scraper) — Apify Store actor (total runs: 247)
- [mercari-japan-search-scraper](https://apify.com/store/actors/mercari-japan-search-scraper) — Apify Store actor (total runs: 187)
- [yahoo-auctions-japan-scraper](https://apify.com/store/actors/yahoo-auctions-japan-scraper) — Apify Store actor (total runs: 173)
- [japan-used-camera-market-scraper](https://apify.com/store/actors/japan-used-camera-market-scraper) — Apify Store actor (total runs: 172)
- [japan-watch-market-scraper](https://apify.com/store/actors/japan-watch-market-scraper) — Apify Store actor (total runs: 156)
- [japan-luxury-brand-market-scraper](https://apify.com/store/actors/japan-luxury-brand-market-scraper) — Apify Store actor (total runs: 154)
- [japan-kakaku-price-search](https://apify.com/store/actors/japan-kakaku-price-search) — Apify Store actor (total runs: 153)
- [japan-used-instrument-market-scraper](https://apify.com/store/actors/japan-used-instrument-market-scraper) — Apify Store actor (total runs: 152)
- [japan-anime-figure-price-data](https://apify.com/store/actors/japan-anime-figure-price-data) — Apify Store actor (total runs: 132)
---

## Apify Store

このリポジトリの Actor は [Apify Store](https://apify.com/fruitful_quintessence) で公開中です。
日本の EC・市場データ収集（Mercari, Yahoo Auctions, Rakuten, SUUMO, DLsite 等）に対応した Apify Actor ディレクトリです。

**Search keywords**: Japan market data, Japanese e-commerce scraping, Apify actors, mercari scraper, rakuten scraper, yahoo auctions japan, suumo real estate, dlsite scraper

