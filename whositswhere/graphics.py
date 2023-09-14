from models import ZoneMap
import pathlib
from PIL import Image, ImageDraw, ImageColor, ImageFont
import logging


class ImageHandler:
    def __init__(self, session, zones: ZoneMap, vip: list[str]):
        self.session = session
        self.zones: ZoneMap = zones
        self.vip = vip
        self.image_paths: list[str] = []

    def get_image(self):
        target = pathlib.Path("results")
        target.mkdir(exist_ok=True)
        for id_, zone in self.zones.items():
            image_path = target / (zone.name + '.png')
            self.session.download_image(id_, image_path)

            im = Image.open(image_path)
            self._draw_names(im, zone)
            im.save(image_path)
            logging.info(f"Created map for {zone.name} - {image_path.absolute()} ")

    def _draw_names(self, im, zone):
        draw = ImageDraw.Draw(im)
        for desk in zone.desks.values():
            x = im.width * desk.x
            y = im.height * desk.y
            if desk.is_free:
                r = 0.02963341 * im.width
                x0 = x - r / 2
                x1 = x + r / 2
                y0 = y - r / 2
                y1 = y + r / 2
                draw.arc((x0, y0, x1, y1), 0, 360, "midnightblue", 3)
            else:
                font = ImageFont.truetype("arial.ttf", 14, encoding="unic")
                color = "darkgreen" if desk.reserved_by.name in self.vip else "darkred"
                draw.text((x, y), desk.reserved_by.name, color, anchor="mm", font=font)
