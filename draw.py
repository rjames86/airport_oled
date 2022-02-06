from email import header
import time
from xml.etree.ElementPath import get_parent_map

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

        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            self.width,
            self.height, 
            i2c, 
            addr=0x3C,
        )

        self.oled.fill(0)
        self.oled.show()

        self.cycle_time = 2

        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        self.font_small = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 8)
        self.font_large = ImageFont.truetype("/Users/rjames/Dropbox/~Inbox/DejaVuSans.ttf", 16)

    def wait(self):
        time.sleep(self.cycle_time)

    def draw_header(self, position, text):
        self.draw.text((position, self.top), text, font=self.font_small, fill=255)

    def draw_body(self, position, text):
        self.draw.text(position, text, font=self.font_large, fill=255)

    def show(self):
        self.oled.image(self.image)
        self.oled.show()

    def scroll_text(self, display_text, header):
        x = 0
        width, _ = self.font_large.getsize(display_text)
        for i in range(0, width // 2, 5):
            self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
            self.draw_header(0, header)
            self.draw_body((x - i, self.top + 12), display_text)
            # self.image.show()
            self.show()
            time.sleep(0.1)

    def write_screen(self):
        x = 0
        ad = AirportData()

        display_texts = {
            "Time":  ad.observation_time,
            "Pressure": ad.sea_level_pressure_mb,
            "Wind":  "%s @ %s kt/hr" % (ad.wind_dir_degrees, ad.wind_speed_kt),
            "Temp":  "%sº C" % ad.temp_c,
        }

        all_pieces_of_text = []
        for key, display_text in display_texts.items():
            header = "%s (%s) - %s" % (ad.station_id, ad.flight_category, key)
            all_pieces_of_text.append((header, display_text))
            width, _ = self.font_large.getsize(display_text)
            if width > self.width:
                self.scroll_text(display_text, header)
            else:
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
                self.draw_header(x + self.padding, header)
                self.draw_body((x + self.padding, self.top + 12), display_text)
                # self.image.show()
                self.show()
                self.wait()