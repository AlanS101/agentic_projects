"""Share prices from the Massive market data API, or a simulator when no key is set.

Set MASSIVE_API_KEY to use live data. Without it, prices come from market_simulator
so the whole trading floor still runs out of the box.
"""

import os
import time
from dotenv import load_dotenv
from massive import RESTClient
from .market_simulator import simulated_price
from .database import read_price_cache, write_price_cache

load_dotenv(override=True)

massive_api_key = os.getenv("MASSIVE_API_KEY")


def _last_trade(client: RESTClient, symbol: str) -> float:
    return float(client.get_last_trade(symbol).price)


def _snapshot(client: RESTClient, symbol: str) -> float:
    snapshot = client.get_snapshot_ticker("stocks", symbol)
    return float(snapshot.min.close or snapshot.prev_day.close)


def _previous_close(client: RESTClient, symbol: str) -> float:
    return float(client.get_previous_close_agg(symbol)[0].close)


# Best price first, prior close last. Lower tier plans reject the earlier calls,
# so we remember the first tier that works and start there next time.
price_methods = [_last_trade, _snapshot, _previous_close]
plan_tier = 0


def _cached_or_raise(symbol: str, error: Exception) -> float:
    cached = read_price_cache(symbol)
    if cached is not None:
        print(f"Massive API unavailable ({error}); using cached price for {symbol}")
        return cached
    raise RuntimeError(f"No real price available for {symbol}") from error


def get_share_price(symbol: str) -> float:
    """Return a share price. Simulator only when no Massive key is configured."""
    if not massive_api_key:
        return simulated_price(symbol)
    if not is_market_open():
        cached = read_price_cache(symbol)
        if cached is not None:
            return cached
    try:
        price = get_share_price_massive(symbol)
        write_price_cache(symbol, price)
        return price
    except Exception as e:
        return _cached_or_raise(symbol, e)


def get_share_price_massive(symbol: str) -> float:
    """Best price the plan allows, remembering the working tier to avoid repeat failures."""
    global plan_tier
    client = RESTClient(massive_api_key)
    for tier in range(plan_tier, len(price_methods)):
        try:
            price = price_methods[tier](client, symbol)
            plan_tier = tier
            return price
        except Exception:
            continue
    raise RuntimeError(f"No Massive price available for {symbol}")


_status_cache: tuple[float, bool] | None = None
STATUS_TTL_SECONDS = 60


def is_market_open() -> bool:
    """Whether the US market is open. A status error means closed, not open."""
    global _status_cache
    if not massive_api_key:
        return True
    now = time.monotonic()
    if _status_cache and now - _status_cache[0] < STATUS_TTL_SECONDS:
        return _status_cache[1]
    try:
        client = RESTClient(massive_api_key)
        opened = client.get_market_status().market == "open"
    except Exception as e:
        print(f"Market status unavailable ({e}); treating the market as closed")
        opened = False
    _status_cache = (now, opened)
    return opened
