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
