"""goo-netの車両データをCSVにダンプするスクリプト（データセット販売用）
   使い方:
     python3 dump.py                       # 全車3ページを dump-YYYYMMDD.csv に出力
     python3 dump.py --model N-BOX         # N-BOXのみ
     python3 dump.py --pages 10 --out dump.csv
"""
import argparse
import asyncio
import csv
import datetime
import os
import sys

import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper import parse_page, fetch_page, BASE_URL

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


async def crawl(max_pages, model=None):
    items = []
    async with httpx.AsyncClient(headers={"User-Agent": UA, "Accept-Language": "ja"}, timeout=30) as client:
        for page in range(1, max_pages + 1):
            url = f"{BASE_URL}/usedcar/" if page == 1 else f"{BASE_URL}/usedcar/index-{page}.html"
            html = await fetch_page(client, url)
            if not html:
                continue
            for it in parse_page(html):
                if it.get("price") is None:
                    continue
                if model:
                    from scraper import _norm
                    if _norm(model).lower() not in _norm(it.get("title", "")).lower():
                        continue
                items.append(it)
            await asyncio.sleep(1)
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="モデル名で絞り込み（例: N-BOX）")
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    items = asyncio.run(crawl(args.pages, args.model))
    out = args.out or f"dump-{datetime.date.today():%Y%m%d}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["itemId", "title", "price_jpy", "detailUrl", "shop"])
        for it in items:
            w.writerow([it.get("itemId"), it.get("title"), it.get("price"), it.get("detailUrl"), it.get("shop")])
    print(f"{len(items)} items -> {out}")


if __name__ == "__main__":
    main()
