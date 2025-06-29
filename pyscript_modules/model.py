import enum


@enum.unique
class Color(enum.Enum):
    GREEN = "#00a964"
    ORANGE = "#ff4D00"
    RED = "#ed1c24"


@enum.unique
class Symbol(enum.Enum):
    # Intermarket
    VIX = "TVC:VIX"
    EURUSD = ""

    # Kassa indices
    DJI = "DJ:DJI"
    NDX = "NASDAQ:NDX"
    SPX = "SP:SPX"
    DAX = "XETR:DAX"
    MDAX = "XETR:MDAX"
    SDAX = "XETR:SDXP"
    TECDAX = "XETR:TDXP"

    # Future indices
    DJI_F = "CBOT_MINI:YM1!"
    NDX_F = "CME_MINI:NQ1!"
    SPX_F = "CME_MINI:ES1!"

    # Crypto
    BITCOIN = "BTC-USD"
    ETHEREUM = "ETH-USD"
    SOLANA = "SOL-USD"


# Symbol collections
intermarket = [
    Symbol.VIX,
    Symbol.EURUSD,
]

usa = [
    Symbol.DJI,
    Symbol.NDX,
    Symbol.SPX,
]

usa_future = [
    Symbol.DJI_F,
    Symbol.NDX_F,
    Symbol.SPX_F,
]

germany = [
    Symbol.DAX,
    Symbol.MDAX,
    Symbol.SDAX,
    Symbol.TECDAX,
]

crypto = [
    Symbol.BITCOIN,
    Symbol.ETHEREUM,
    Symbol.SOLANA,
]

symbol_sets = {
    "intermarket": intermarket,
    "usa": usa,
    "usa_future": usa_future,
    "germany": germany,
    "crypto": crypto,
}
