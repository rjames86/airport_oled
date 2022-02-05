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
        padding = 0
        top = padding
        bottom = self.height - padding
        x = 0

        ad = AirportData()

        font_small = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 8)
        font_large = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 16)

        display_texts = {
            "Pressure": ad.sea_level_pressure_mb,
            "Wind":  "%s @ %s kt/hr" % (ad.wind_dir_degrees, ad.wind_speed_kt),
            "Temp":  "%sº C" % ad.temp_c,
        }
        
        for key, display_text in display_texts.items():
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw.text((x, top), "%s (%s) - %s" % (ad.station_id, ad.flight_category, key),  font=font_small, fill=255)
            self.draw.text((x, top+12), display_text, font=font_large, fill=255)
            self.image.show()
            time.sleep(3)