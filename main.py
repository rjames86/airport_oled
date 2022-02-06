from draw import OLEDDraw
from config import ON_TIME, OFF_TIME
import datetime
import time

now = datetime.datetime.now()

start_hour, start_minute = ON_TIME
off_hour, off_minute = OFF_TIME

on_time = now.replace(hour=start_hour, minute=start_minute, second=0)
off_time = now.replace(hour=off_hour, minute=off_minute, second=0)

ONE_HOUR = 1 * 60 * 60

if __name__ == "__main__":
    d = OLEDDraw()
    try:
        while True:
            if now > on_time and now < off_time:
                d.write_screen()
            else:
                print("Turning off for the night...")
                d.clear_screen()
                time.sleep(ONE_HOUR)
    except KeyboardInterrupt:
        d.clear_screen()
