"""毎日チェックの単体実行スクリプト（cron用）
   使い方: python3 check.py
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from checker import check_all


async def main():
    hits, count = await check_all()
    print(f"[car-price-alert] checked {count} alerts, hits={hits}")
    return 0 if hits == 0 else 0  # ヒット有無に関わらず正常終了（通知はメール側）


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
