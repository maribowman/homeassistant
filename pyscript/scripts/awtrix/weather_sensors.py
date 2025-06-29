import mqtt


@state_trigger("sensor.mari_weather_temperature")  # noqa - F821
@state_trigger("sensor.living_room_weather_temperature")  # noqa F821
@state_trigger("sensor.balcony_side_weather_temperature")  # noqa F821
@state_trigger("sensor.window_side_weather_temperature")  # noqa F821
def temperature_forwarder(**kwargs) -> None:
    try:
        sensor_entity = kwargs["var_name"]
        temperature = float(kwargs["value"])
    except Exception:
        log.debug(  # noqa - F821
            f"Sensor value for `{kwargs['var_name']
                }` is not numeric: `{kwargs['value']}`"
        )
        return

    text = f"{temperature}"

    if sensor_entity == "sensor.mari_weather_temperature":
        topic = "awtrix_1/custom/temperature"

    elif sensor_entity == "sensor.living_room_weather_temperature":
        topic = "awtrix_2/custom/temperature"

    elif sensor_entity in [
        "sensor.balcony_side_weather_temperature",
        "sensor.window_side_weather_temperature",
    ]:
        topic = "awtrix_2/custom/temperature_outside"
        text = (
            f"{sensor.window_side_weather_temperature} -"  # noqa F821
            + f" {sensor.balcony_side_weather_temperature}"  # noqa F821
        )

    else:
        log.warn(f"Could not map `{sensor_entity}` to entity")  # noqa F821
        return

    if temperature <= -5:
        icon = "thermometer_1"
    elif -5 < temperature and temperature <= 0:
        icon = "thermometer_2"
    elif 0 < temperature and temperature <= 10:
        icon = "thermometer_3"
    elif 10 < temperature and temperature <= 20:
        icon = "thermometer_4"
    elif 20 < temperature and temperature <= 30:
        icon = "thermometer_5"
    elif 30 < temperature:
        icon = "thermometer_6"
    else:
        log.warn("Could not map temperature value to icon")  # noqa F821

    mqtt.publish(
        topic=topic,
        payload={
            "icon": icon,
            "text": text,
        },
    )


@state_trigger("sensor.mari_weather_humidity")  # noqa F821
@state_trigger("sensor.living_room_weather_humidity")  # noqa F821
def humidity_forwarder(**kwargs) -> None:
    if kwargs["var_name"] == "sensor.mari_weather_humidity":
        topic = "awtrix_1/custom/humidity"
    elif kwargs["var_name"] == "sensor.living_room_weather_humidity":
        topic = "awtrix_2/custom/humidity"

    mqtt.publish(
        topic=topic,
        payload={
            "icon": "humidity",
            "text": f"{kwargs['value']}%",
        },
    )
