from email import header
import time
from xml.etree.ElementPath import get_parent_map

import adafruit_ssd1306
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont

from airport import AirportData

class OLEDDraw:
    def __init__(self):
        self.width = 128
        self.height = 64
        self.border = 5

        self.padding = 0
        self.top = self.padding
        self.bottom = self.height - self.padding

        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            self.width,
            self.height, 
            i2c, 
            addr=0x3C,
        )

        self.oled.fill(0)
        self.oled.show()

        self.cycle_time = 4

        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.font_small = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 12)
        self.font_large = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 36)

    def wait(self, wait):
        time.sleep(wait)

    def draw_header(self, position, text):
        self.draw.text((position, self.top), text, font=self.font_small, fill=255)

    def draw_body(self, position, text):
        self.draw.text(position, text, font=self.font_large, fill=255)

    def show(self, wait):
        self.oled.image(self.image)
        self.oled.show()
        self.wait(wait)

    def scroll_text(self, display_text, header):
        x = 0
        width, _ = self.font_large.getsize(display_text)
        # Start at negative half the screen so that the scrolling text starts at the middle of the screen
        for i in range(0, (width - self.width) + self.border, 3):
            if i == 0:
                self.wait(0.5)
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw_header(0, header)
            self.draw_body((x - i, self.top + 12), display_text)
            # self.image.show()
            self.show(0.02)
        self.wait(1)

    def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()
    
    def write_screen(self):
        x = 0
        ad = AirportData()

        display_texts = {
            "Time":  ad.observation_time,
            "Pressure": ad.sea_level_pressure_mb,
            "Wind":  "%s @ %s kt/hr" % (ad.wind_dir_degrees, ad.wind_speed_kt),
            "Temp":  "%sº C" % ad.temp_c,
            "Category":  ad.flight_category,
        }

        all_pieces_of_text = []
        for key, display_text in display_texts.items():
            header = "%s - %s" % (ad.station_id, key)
            all_pieces_of_text.append((header, display_text))
            width, _ = self.font_large.getsize(display_text)
            if width > self.width:
                self.scroll_text(display_text, header)
            else:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
                self.draw_header(x + self.padding, header)
                self.draw_body((x + self.padding, self.top + 12), display_text)
                # self.image.show()
                self.show(self.cycle_time)
