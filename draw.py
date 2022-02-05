import time

# import adafruit_ssd1306
# import board
# import digitalio
from PIL import Image, ImageDraw, ImageFont

from airport import AirportData

class OLEDDraw:
    def __init__(self):
        self.width = 128
        self.height = 32
        self.border = 5

        # i2c = board.I2C()
        # self.oled = adafruit_ssd1306.SSD1306_I2C(
        #     self.width,
        #     self.height, 
        #     i2c, 
        #     addr=0x3C,
        # )

        # self.oled.fill(0)
        # self.oled.show()

        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def write_screen(self):
        padding = -2
        top = padding
        bottom = self.height - padding
        x = 0

        ad = AirportData()

        font = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 8)
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((x, top),       "Airport: %s (%s)" % (ad.station_id, ad.flight_category),  font=font, fill=255)
        self.draw.text((x, top+16),    "Time: " + ad.observation_time,  font=font, fill=255)
        self.draw.text((x, top+8),     "Pressure: " + ad.sea_level_pressure_mb, font=font, fill=255)
        self.draw.text((x, top+25),    "Wind: %s @ %s kt/hr" % (ad.wind_dir_degrees, ad.wind_speed_kt),  font=font, fill=255)
        self.image.show()