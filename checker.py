"""価格チェックの中核ロジック（FastAPI 非依存）。

2026-10-12: 元は app.py に同居していたため、cron 用の check.py が
`from app import check_all` を実行した時点で fastapi の import が走り、
venv に fastapi が無い環境では `ModuleNotFoundError` で停止していた
（実測: 2026-10-04 から8日間 cron が失敗し続けた）。

Web 層（FastAPI）と取得ロジックを分離し、cron はこちらだけを import する。
"""

from __future__ import annotations

import asyncio
import json

import httpx

from db import get_alerts, init_db, update_checked
from notifier import send_alert
from scraper import search_model

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


async def check_all() -> tuple[int, int]:
    """登録済みアラートを全て確認し (ヒット件数, アラート件数) を返す。"""
    init_db()
    alerts = get_alerts()
    total_hits = 0
    async with httpx.AsyncClient(
        headers={"User-Agent": UA, "Accept-Language": "ja"}, timeout=30
    ) as client:
        for alert in alerts:
            matches = await search_model(client, alert["model"], max_pages=3)
            hits = [m for m in matches if m["price"] <= alert["max_price"]]
            if hits:
                await asyncio.to_thread(send_alert, alert, hits)
            update_checked(alert["id"], json.dumps(hits[:5], ensure_ascii=False))
            total_hits += len(hits)
            await asyncio.sleep(2)
    return total_hits, len(alerts)
