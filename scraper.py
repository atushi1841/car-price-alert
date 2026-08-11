import httpx
import re
import unicodedata
import datetime
from bs4 import BeautifulSoup

BASE_URL = "https://www.goo-net.com"

def _norm(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u2212", "-").replace("\uff0d", "-").replace("\u2010", "-").replace("\u2011", "-")
    return s

async def fetch_page(client, url):
    try:
        resp = await client.get(url)
        if resp.status_code != 200:
            return None
        resp.encoding = "euc-jp"
        return resp.text
    except Exception:
        return None

def _extract_price_from_text(text, label):
    if not text:
        return None
    pos = text.find(label)
    if pos == -1:
        return None
    after = text[pos:].replace(" ", "").replace("\u3000", "")
    m = re.search(r"([\d,]+\.?\d*)\s*万円", after)
    if not m:
        return None
    try:
        v = float(m.group(1).replace(",", ""))
        return int(v * 10000)
    except Exception:
        return None


def parse_page(html):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items = []
    cards = soup.select("div.search-card")
    for card in cards:
        detail_link = card.select_one('a[href*="/usedcar/spread/"]')
        if not detail_link:
            continue
        href = detail_link.get("href")
        if not href:
            continue
        m = re.search(r"/usedcar/spread/goo/\d+/(\d+)\.html", href)
        item_id = m.group(1) if m else None
        title_elem = card.select_one("h3.search-card__title a") or card.find("h3")
        title = title_elem.get_text(strip=True) if title_elem else None
        card_text = card.get_text(" ", strip=True)
        price = _extract_price_from_text(card_text, "支払総額")
        if price is None:
            price = _extract_price_from_text(card_text, "車両本体価格")
        shop_elem = card.select_one('a[href*="/usedcar_shop/"]')
        shop = shop_elem.get_text(strip=True) if shop_elem else None
        if href.startswith("http"):
            detail_url = href
        else:
            detail_url = BASE_URL + href
        item = {
            "itemId": item_id,
            "title": title,
            "price": price,
            "detailUrl": detail_url,
            "shop": shop,
        }
        items.append(item)
    return items

async def search_model(client, model, max_pages=3):
    found = []
    normalized_model = _norm(model).lower()
    for page in range(1, max_pages + 1):
        if page == 1:
            url = f"{BASE_URL}/usedcar/"
        else:
            url = f"{BASE_URL}/usedcar/index-{page}.html"
        html = await fetch_page(client, url)
        if not html:
            continue
        for it in parse_page(html):
            if it.get("price") is None:
                continue
            title_norm = _norm(it.get("title", "")).lower()
            if normalized_model in title_norm:
                found.append(it)
    return found
