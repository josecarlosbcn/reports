import PIL.Image, PIL.ImageDraw, PIL.ImageFont
from constants import IMAGES
import os, locale


class ShotChartImage:
    '''Only one of the two parameters can be None. Only one of two parameters cannot be distinct to None'''
    def __init__(self, file):
        self.file = file
        self.image = PIL.Image.open(file).convert("RGB")
        #Put image over background
        # self.background.paste(self.image)
        # self.image = self.background
        size = self.image.size
        self.w = size[0]
        self.h = size[1]

    def get_color(self, x, y):
        color = self.image.getpixel((int(x),int(y)))
        color = ("#%02x%02x%02x" % color).upper()
        return color

    @staticmethod
    def get_data(d, s, type):
        total_shoots = len(d)
        data = d.query(f"position == '{type}'")
        total_shoots_position = len(data)
        if total_shoots_position > 1:
            data = d.query(f"position == '{type}' and m == 1")
            total_shoots_position_scored = len(data)
        else:
            total_shoots_position_scored = total_shoots_position
        data = s.query(f"position == '{type}'")
        total_season_shoots = len(data)
        data = s.query(f"position == '{type}' and m == 1")
        total_season_shoots_scored = len(data)
        #locale.format('%0.2f', d, grouping=True) to show data in spanish format
        #percentage of shoots made if in that position
        try:
            p_shoots = locale.format('%0.2f', round(total_shoots_position/total_shoots*100, 2), grouping=True) + "%"
        except ZeroDivisionError:
            p_shoots = "0,00%"
        #print(f"% lanzamientos desde la posición {type}: {p_shoots} lanzados/convertidos {total_shoots_position}/{total_shoots}")
        #percentage of shots scored in that position
        try:
            p_shoots_scored = locale.format("%0.2f", round(total_shoots_position_scored/(total_shoots_position)*100, 2), grouping=True) + "%"
        except ZeroDivisionError:
            p_shoots_scored = "0,00%"
        #print(f"% lanzamientos anotados desde la posición {type}: {p_shoots_scored} anotados/lanzados {total_shoots_position_scored}/{total_shoots_position}")
        #percentate of shoots scored in that position (all teams)
        try:
            p_shoots_scored_season = locale.format("%0.2f", round(total_season_shoots_scored/total_season_shoots*100, 2), grouping=True) + "%"
        except ZeroDivisionError:
            p_shoots_scored_season = "0,00%"
        #print(f"% lanzamientos anotados en la competición {type}: {p_shoots_scored_season} anotados/lanzados {total_season_shoots_scored}/{total_season_shoots}")
        return {
            "p_shoots_position" : p_shoots,
            "p_scored_position" : p_shoots_scored,
            "p_season_scored_position": p_shoots_scored_season
        }

    @staticmethod
    def remove_image(name):
        os.remove(name)

    def resize_from_width(self, width):
        (w, h) = self.image.size
        height = h*(width*100/w)/100
        self.image = self.image.resize((int(width), int(height)))
        self.w = width
        self.h = height

    def save_image(self, name):
        self.image.save(name, "png")

    def set_background(self, w, h, r, g, b):
        '''We create a bckground with a size defined by w: width and h: height and a color background defined by the variables r, g, b'''
        self.background = PIL.Image.new("RGB", (w, h), (r, g, b))

    def set_data_over_image(self, d, s):
        '''Set the data over the image. params d and s are the data. Both are DataFrames.
        d: Contains data of a team or a player
        s: Contains data of a whole season'''
        i = PIL.ImageDraw.Draw(self.image)
        self.set_c3l(i,d, s)
        self.set_c3r(i,d, s)
        self.set_pc(i,d, s)
        self.set_mbl(i,d, s)
        self.set_mbr(i,d, s)
        self.set_pl(i,d, s)
        self.set_pr(i,d, s)
        self.set_mel(i,d, s)
        self.set_mer(i,d, s)
        self.set_e3l(i,d, s)
        self.set_e3r(i,d, s)
        self.set_ce3l(i,d, s)
        self.set_ce3r(i,d, s)
        self.set_legend(i)

    def set_c3l(self, image, d, s):
        data = self.get_data(d, s, "C3L")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-185
        y = 10
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))
        draw = PIL.ImageDraw.Draw(self.image)
        draw.line([(15, y+20), (x-10, y+20)], fill=(0, 0, 0), width=2)
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 28)
        draw.text((10, y+3), "<", fill=(0, 0, 0), font=fnt)

    def set_c3r(self, image, d, s):
        data = self.get_data(d, s, "C3R")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w - 100
        y = 10
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))
        draw = PIL.ImageDraw.Draw(self.image)
        draw.line([(self.w - 15, y+20), (self.w - 60, y+20)], fill=(0, 0, 0), width=2)
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 28)
        draw.text((self.w - 25, y+3), ">", fill=(0, 0, 0), font=fnt)

    def set_pc(self, image, d, s):
        data = self.get_data(d, s, "PC")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-20
        y = 70
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_mbl(self, image, d, s):
        data = self.get_data(d, s, "MBL")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-185
        y = 80
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_mbr(self, image, d, s):
        data = self.get_data(d, s, "MBR")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2+150
        y = 80
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_pl(self, image, d, s):
        data = self.get_data(d, s, "PL")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-70
        y = 80
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_pr(self, image, d, s):
        data = self.get_data(d, s, "PR")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2+35
        y = 80
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_mel(self, image, d, s):
        data = self.get_data(d, s, "MEL")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-95
        y = 200
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_mer(self, image, d, s):
        data = self.get_data(d, s, "MER")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2+45
        y = 200
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_e3l(self, image, d, s):
        data = self.get_data(d, s, "E3L")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = 10
        y = 180
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_e3r(self, image, d, s):
        data = self.get_data(d, s, "E3R")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w-50
        y = 180
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_ce3l(self, image, d, s):
        data = self.get_data(d, s, "Ce3L")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2-100
        y = 275
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_ce3r(self, image, d, s):
        data = self.get_data(d, s, "Ce3R")
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 12)
        x = self.w/2+50
        y = 275
        image.text((x, y), data["p_shoots_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*1), data["p_scored_position"], font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), data["p_season_scored_position"], font=fnt, fill=(0, 0, 0))

    def set_legend(self, image):
        fnt = PIL.ImageFont.truetype(IMAGES.FONTS_ROUTE + "Roboto-Medium.ttf", 11)
        x = 10
        y = self.h - 70
        image.text((x, y+15*1), "% de tiros lanzados desde esa posición", font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*2), "% de tiros anotados desde esa posición", font=fnt, fill=(0, 0, 0))
        image.text((x, y+15*3), "% de tiros anotados desde esa posición (todas las jugadoras de la competición)", font=fnt, fill=(0, 0, 0))
