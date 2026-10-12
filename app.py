import asyncio
import os
import datetime
import json
import traceback

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

import httpx

from scraper import search_model
from db import init_db, get_alerts, add_alert, update_checked
from notifier import send_alert
from checker import check_all

app = FastAPI(title="Japan Car Price Alert")

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

@app.on_event("startup")
async def startup_event():
    init_db()
    asyncio.create_task(daily_loop())

async def daily_loop():
    while True:
        await asyncio.sleep(24 * 60 * 60)
        try:
            await check_all()
        except Exception:
            traceback.print_exc()

@app.get("/", response_class=HTMLResponse)
async def index():
    html = """<!DOCTYPE html>
<html lang="ja">
<head><meta charset="utf-8"><title>中古車価格アラート</title></head>
<body>
<h1>中古車価格アラート登録</h1>
<form method="post" action="/alerts">
  <label>車種 (例: クラウン) <input type="text" name="model" required></label><br>
  <label>希望上限価格 (円) <input type="number" name="max_price" required></label><br>
  <label>メールアドレス <input type="email" name="email" required></label><br>
  <button type="submit">登録</button>
</form>
<p><a href="/alerts">登録済みアラート一覧</a></p>
<p><a href="/run-check" onclick="fetch('/run-check',{method:'POST'}).then(r=>r.text()).then(t=>document.body.insertAdjacentHTML('beforeend','<hr>'+t));return false;">今すぐチェック実行</a></p>
</body>
</html>"""
    return HTMLResponse(html)

@app.post("/alerts")
async def create_alert(model: str = Form(...), max_price: int = Form(...), email: str = Form(...)):
    add_alert(model, max_price, email)
    return RedirectResponse("/alerts", status_code=303)

@app.get("/alerts", response_class=HTMLResponse)
async def alerts_list():
    rows = get_alerts()
    table_rows = ""
    for alert in rows:
        table_rows += f"""<tr>
<td>{alert['id']}</td>
<td>{alert['model']}</td>
<td>{alert['max_price']} 円</td>
<td>{alert['email']}</td>
<td>{alert.get('last_checked_at') or '未実行'}</td>
<td>{alert.get('last_found') or ''}</td>
</tr>"""
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head><meta charset="utf-8"><title>アラート一覧</title></head>
<body>
<h1>登録済みアラート</h1>
<table border="1">
<tr><th>ID</th><th>車種</th><th>上限価格</th><th>メール</th><th>最終チェック</th><th>最後のヒット</th></tr>
{table_rows}
</table>
<p><a href="/">新規登録</a></p>
</body>
</html>"""
    return HTMLResponse(html)

@app.post("/run-check", response_class=HTMLResponse)
async def run_check():
    total_hits, count = await check_all()
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head><meta charset="utf-8"><title>チェック結果</title></head>
<body>
<h2>チェック完了</h2>
<p>{count} 件のアラートを確認しました。ヒット: {total_hits} 件</p>
<p><a href="/alerts">アラート一覧へ</a></p>
</body>
</html>"""
    return HTMLResponse(html)
