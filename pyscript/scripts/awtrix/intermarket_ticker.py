import sys

import mqtt

if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")
import custom_requests as custom
import model


@time_trigger("cron(*/5 8-14 * * 1-5)", kwargs={"market": "usa_future"})  # noqa F821
@time_trigger("cron(*/5 15-23 * * 1-5)", kwargs={"market": "usa"})  # noqa F821
@time_trigger("cron(*/5 8-21 * * 1-5)", kwargs={"market": "germany"})  # noqa F821
def update_intermarket_change(**kwargs) -> None:
    market = kwargs["market"]

    text = []
    positive_counter = 0
    negative_counter = 0

    for symbol in model.symbol_sets[market]:
        try:
            response = task.executor(custom.get_intermarket_change, symbol)  # noqa F821
            change = response.json()["change"]

            if change >= 0:
                color = model.Color.GREEN.value
                positive_counter += 1
            else:
                color = model.Color.RED.value
                negative_counter += 1

            text.append(
                {
                    "t": f"{symbol.name} {round(change, 1)}% ",
                    "c": color,
                }
            )
        except Exception as e:
            log.error(e)  # noqa F821

    if not text:
        log.error(f"No intermarket data to show for `{market}`")  # noqa F821
        return

    mqtt.publish(
        topic=f"awtrix_1/custom/{market.removesuffix('_future')}",
        payload={
            "icon": market.removesuffix("_future"),
            "text": text,
            "lifetime": 300,
            "repeat": 3,
        },
    )
