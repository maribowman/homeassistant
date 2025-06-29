import model
from http import HTTPStatus

import requests

# Changes to this module require a HA restart!


# INTERMARKET
def get_intermarket_change(symbol: model.Symbol) -> requests.Response:
    """
    https://www.tradingview.com/markets/indices/quotes-all/
    """
    response = requests.get(
        url=f"https://scanner.tradingview.com/symbol?symbol={symbol.value}&fields=change")
    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Could not get {symbol.value} change, received status {
                        response.status_code}")
    return response


# CRYPTO
def get_crypto_prices() -> requests.Response:
    """
    https://developers.coindesk.com/documentation/data-api/spot_v1_latest_tick
    """
    symbols = ",".join([coin.value for coin in model.crypto])
    response = requests.get(
        url=f"https://data-api.coindesk.com/spot/v1/latest/tick?market=coinbase&instruments={symbols}&apply_mapping=true")
    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Could not get crypto prices, received status {
                        response.status_code}")
    return response


# 3D PRINTER - Klipper
def get_printer_status() -> requests.Response:
    """
    https://moonraker.readthedocs.io/en/latest/web_api/#get-printer-status
    """
    response = requests.get(url="http://192.168.0.189/api/printer")
    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Could not get printer status, received status {
                        response.status_code}")
    return response


def shutdown_printer() -> requests.Response:
    """
    https://moonraker.readthedocs.io/en/latest/web_api/#shutdown-the-operating-system
    """
    response = requests.post(url="http://192.168.0.189/machine/shutdown")
    if response.status_code != HTTPStatus.OK:
        raise Exception(f"Could not shutdown printer, received status {
                        response.status_code}")
    return response
