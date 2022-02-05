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

        self.padding = 0
        self.top = self.padding
        self.bottom = self.height - self.padding

        # i2c = board.I2C()
        # self.oled = adafruit_ssd1306.SSD1306_I2C(
        #     self.width,
        #     self.height, 
        #     i2c, 
        #     addr=0x3C,
        # )

        # self.oled.fill(0)
        # self.oled.show()

        self.cycle_time = 3

        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.font_small = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 8)
        self.font_large = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 16)

    def wait(self):
        time.sleep(self.cycle_time)


    def scroll_text(self, display_text, header):
        x = 0
        width, _ = self.font_large.getsize(display_text)
        for i in range(0, width - self.width + self.border, 5):
            print("i", i)
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw.text((0, self.top), header,  font=self.font_small, fill=255)
            self.draw.text((x - i, self.top + 12), display_text, font=self.font_large, fill=255)
            self.image.show()
            time.sleep(0.5)
        self.wait()

    def write_screen(self):
        x = 0

        ad = AirportData()

        display_texts = {
            "Time":  ad.observation_time,
            "Pressure": ad.sea_level_pressure_mb,
            "Wind":  "%s @ %s kt/hr" % (ad.wind_dir_degrees, ad.wind_speed_kt),
            "Temp":  "%sº C" % ad.temp_c,
        }

        for key, display_text in display_texts.items():
            header = "%s (%s) - %s" % (ad.station_id, ad.flight_category, key)

            width, _ = self.font_large.getsize(display_text)
            if width > self.width:
                self.scroll_text(display_text, header)
            else:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
                self.draw.text((x, self.top), header, font=self.font_small, fill=255)
                self.draw.text((x, self.top + 12), display_text, font=self.font_large, fill=255)
                self.image.show()
                self.wait()