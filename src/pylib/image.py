import math
from random import randint
from io import BytesIO

from PIL import Image, ImageDraw, ImageSequence, ImageFont


def scale_area(area, scale, max_size=None):
    center = [(area[0] + area[2]) / 2, (area[1] + area[3]) / 2]
    width = (area[2] - area[0]) * scale
    height = (area[3] - area[1]) * scale
    left = int(center[0] - width / 2)
    top = int(center[1] - height / 2)
    right = int(center[0] + width / 2)
    bottom = int(center[1] + height / 2)
    return [
        left if left >= 0 else 0,
        top if top >= 0 else 0,
        right if max_size is None or right <= max_size[0] else max_size[0],
        bottom if max_size is None or bottom <= max_size[1] else max_size[1]
    ]


def compress_image(fp, total_pixeles=1048576, quality=85):
    if isinstance(fp, bytes):
        fp = BytesIO(fp)
    im = Image.open(fp)
    if im.mode != "RGB":
        im = im.convert("RGB")

    ratio = (im.size[0] * im.size[1]) / total_pixeles
    if ratio > 1:
        size = [int(v / math.sqrt(ratio)) for v in im.size]
    else:
        size = list(im.size)
    tm = im.copy()
    tm.thumbnail(size, Image.ANTIALIAS)
    out = BytesIO()
    tm.save(out, "JPEG", quality=quality)

    return out.getvalue(), size


def print_watermark(fp, text, position=None, font=None, quality=85):
    if isinstance(fp, bytes):
        fp = BytesIO(fp)
    im = Image.open(fp)
    if im.format == 'GIF':
        return fp.getvalue() if isinstance(fp, BytesIO) else fp.read()

    water_im = Image.new("RGBA", im.size)
    water_draw = ImageDraw.ImageDraw(water_im)
    if isinstance(font, str):
        font = ImageFont.truetype(font, 16 + int(im.size[0] / 100))
    if not position:
        water_size = water_draw.textsize(text, font=font)
        position = (im.size[0] - water_size[0] * 1.05,
                    im.size[1] - water_size[1] * 1.2)
    water_draw.text(position, text, font=font)
    water_mask = water_im.convert("L").point(lambda x: min(x, 160))
    water_im.putalpha(water_mask)

    if im.format == 'GIF':
        for frame in ImageSequence.Iterator(im):
            frame.paste(water_im, None, water_im)
    else:
        im.paste(water_im, None, water_im)
    out = BytesIO()
    im.save(out, im.format, quality=quality, **im.info)

    return out.getvalue()


def captcha_image(text, font, font_size=50, image_size=(240, 80),
                  save_format='JPEG', save_path=None):
    im = Image.new('RGB', image_size, 0xffffff)
    d = ImageDraw.Draw(im)

    for _ in range(randint(200, 300)):
        d.point((randint(0, im.size[0]), randint(0, im.size[1])),
                fill=randint(0, 0xffffff))

    for _ in range(randint(5, 15)):
        d.line(
            (randint(0, im.size[0]), randint(0, im.size[1]),
                randint(0, im.size[0]), randint(0, im.size[1])),
            fill=randint(0, 0xffffff))

    font = ImageFont.truetype(font, font_size)
    text_size = font.getsize(text)
    if image_size[0] < text_size[0] or image_size[1] < text_size[1]:
        raise Exception("image too small: {} {}".format(image_size, text_size))
    d.text(
        ((image_size[0] - text_size[0]) / 2,
            (image_size[1] - text_size[1]) / 2),
        text, font=font, fill=randint(0, 0xffff00))

    if save_path:
        im.save(save_path, format=save_format)
    else:
        out = BytesIO()
        im.save(out, format=save_format)
        return out.getvalue()
