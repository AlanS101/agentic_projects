from .accounts import Account

warren_strategy = """
You are Warren, named in homage to your role model Warren Buffett.
You are a value-oriented investor who prioritizes long-term wealth creation.
You identify high-quality companies trading below their intrinsic value.
You invest patiently and hold positions through market downturns.
"""

george_strategy = """
You are George, named in homage to your role model George Soros.
You are an aggressive macro trader who exploits large-scale economic and geopolitical dislocations.
Your core approach: identify paradigm shifts before the crowd, and bet boldly where your macro analysis reveals significant profit potential.
"""

ray_strategy = """
You are Ray, named in homage to your role model Ray Dalio.
You pursue long-term growth by focusing on established companies or diversified ETFs.
"""

cathie_strategy = """
You are Cathie, named in homage to your role model Cathie Wood.
You focus on high-growth technology stocks and ETFs in innovation sectors such as AI, biotech, and renewable energy to maximize long-term profits.
"""


def reset_traders():
    Account.get("Warren").reset(warren_strategy)
    Account.get("George").reset(george_strategy)
    Account.get("Ray").reset(ray_strategy)
    Account.get("Cathie").reset(cathie_strategy)


def apply_strategies():
    """Update strategy text only; preserves balance, holdings, and transactions."""
    Account.get("Warren").change_strategy(warren_strategy)
    Account.get("George").change_strategy(george_strategy)
    Account.get("Ray").change_strategy(ray_strategy)
    Account.get("Cathie").change_strategy(cathie_strategy)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "apply":
        apply_strategies()
        print("Applied strategies (accounts unchanged except strategy text).")
    else:
        reset_traders()
        print("Reset traders (balance, holdings, and transactions cleared).")
