import enum
import os
import time
import bambulabs_api as bl

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    IP = os.getenv("IP")
    ACCESS_CODE = os.getenv("ACCESS_CODE")
    SERIAL = os.getenv("SERIAL")
    printer = bl.Printer(
        ip_address=IP,
        access_code=ACCESS_CODE,
        serial=SERIAL,
    )

    printer.mqtt_start()
    time.sleep(2)

    # TODO Use enum correctly -> maps to UNKNOWN
    status = bl.GcodeState(printer.get_state())
    print(status)
    while status in [bl.GcodeState.PREPARE, bl.GcodeState.RUNNING, bl.GcodeState.PAUSE]:
        break  # TODO: Remove
        time.sleep(60)
        printer.turn_light_off()
        # TODO: Publish details as homeassistant sensor values
        percentage = printer.get_percentage()
        layer_num = printer.current_layer_num()
        total_layer_num = printer.total_layer_num()
        remaining_time = printer.get_time()
        status = bl.GcodeState(printer.get_state())

    bed_temperature = printer.get_bed_temperature()
    nozzle_temperature = printer.get_nozzle_temperature()
    while nozzle_temperature > 50:
        time.sleep(30)
        nozzle_temperature = printer.get_nozzle_temperature()

    printer.mqtt_stop()

    # TODO: Turn printer off
