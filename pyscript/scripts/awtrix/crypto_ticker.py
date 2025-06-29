import sys

import mqtt

if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")
import custom_requests as custom
import model


@time_trigger("cron(* * * * *)")  # noqa F821
def update_crypto_prices() -> None:
    try:
        response = task.executor(custom.get_crypto_prices)  # noqa F821
        response_data = response.json()["Data"]
    except Exception as e:
        log.error(e)  # noqa F821
        return

    for coin in model.crypto:
        open_: float = response_data[coin.value]["CURRENT_DAY_OPEN"]
        current: float = response_data[coin.value]["PRICE"]
        change: float = response_data[coin.value]["CURRENT_DAY_CHANGE_PERCENTAGE"]

        mqtt.publish(
            topic=f"awtrix_1/custom/{coin.name.lower()}",
            payload={
                "icon": coin.name.lower(),
                "text": f"{round(change, 1)}%  {round(current, 1)}$",
                "color": model.Color.GREEN.value if current >= open_ else model.Color.RED.value,
                "lifetime": 300,
                "repeat": 2,
            },
        )
