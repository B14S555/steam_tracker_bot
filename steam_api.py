import requests


def get_price(appid: int, market_hash_name: str):
    """
    Возвращает (low, median) в виде строк, как их даёт Steam, либо (None, None)
    """
    url = (
        "https://steamcommunity.com/market/priceoverview/"
        f"?currency=1&appid={appid}&market_hash_name={market_hash_name}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Steam API error:", e)
        return None, None

    if not data.get("success"):
        return None, None

    return data.get("lowest_price"), data.get("median_price")
