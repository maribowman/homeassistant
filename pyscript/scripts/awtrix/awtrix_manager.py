from datetime import datetime

import mqtt


@state_trigger("sensor.awtrix_2_battery")  # noqa F821
def dynamic_power(**kwargs) -> None:
    if not kwargs["value"].isnumeric():
        return

    if int(kwargs["value"]) > 80:
        switch.turn_off(entity_id="switch.living_room_awtrix")  # noqa F821
    elif int(kwargs["value"]) < 40:
        switch.turn_on(entity_id="switch.living_room_awtrix")  # noqa F821


@service  # noqa F821
@time_trigger("cron(0 6,22 * * *)")  # noqa F821
def matrix_nightmode(**kwargs) -> None:
    for topic in [
        "awtrix_1/power",
        "awtrix_2/power",
    ]:
        mqtt.publish(
            topic=topic,
            payload={
                "power": datetime.now().hour > 5 and datetime.now().hour < 22,
            },
        )
