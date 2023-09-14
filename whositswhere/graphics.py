from models import ZoneMap
import pathlib
from PIL import Image, ImageDraw, ImageColor, ImageFont, ImageOps
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
            x = int(im.width * desk.x)
            y = int(im.height * desk.y)
            if desk.is_free:
                r = 0.03 * im.width
                x0 = x - r / 2
                x1 = x + r / 2
                y0 = y - r / 2
                y1 = y + r / 2
                draw.arc((x0, y0, x1, y1), 0, 360, "midnightblue", 3)
            else:
                # draw a text on a new canvas
                txt_canvas = Image.new('L', (500, 50))
                text_draw = ImageDraw.Draw(txt_canvas)
                font = ImageFont.truetype("arial.ttf", 18, encoding="unic")
                text_draw.text((0, 0), desk.reserved_by.name, font=font, fill=255)

                # rotate to avoid overlapping letters
                w = txt_canvas.rotate(-12, expand=True)

                # offset to kind of align the name on the middle of the chairs
                x_offset = int(-len(desk.reserved_by.name) * 0.5 * 18 / 2)
                y_offset = -20
                # paste the text on the image
                color = "darkgreen" if desk.reserved_by.name in self.vip else "darkred"
                im.paste(ImageOps.colorize(w, "black", color), (x + x_offset, y + y_offset), w)



