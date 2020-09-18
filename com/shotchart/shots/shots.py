from com.shotchart.shots.shot_colors import ShotColors
from constants import COMPETITIONS, IMAGES
from com.shotchart.images.shotchartimage import ShotChartImage
from operator import itemgetter
import codecs


class Shots:
    def __init__(self, competition):
        sc = ShotColors()
        self.competition = competition
        self.colors = sc.maristas_colors

    def add_column(self, name_column):
        self.df[name_column] = None

    def load_images(self):
        if self.competition == COMPETITIONS.LF1 or self.competition == COMPETITIONS.LF2:
            left = ShotChartImage(IMAGES.FEB_LEFT_COLOUR_MAP)
            right = ShotChartImage(IMAGES.FEB_RIGHT_COLOUR_MAP)
            return (left, right)
        else:
            img = ShotChartImage(IMAGES.FIBA_COLOUR_MAP)
            return img

    def select_image(self, images, team):
        '''Return the image over we are going to take the color of the pixel. This dependes of the competition and if the team is playing at home or
        like visitor'''
        if (self.competition == COMPETITIONS.LF1 or self.competition == COMPETITIONS.LF2) and team == 0:
            return images[0]
        if (self.competition == COMPETITIONS.LF1 or self.competition == COMPETITIONS.LF2) and team == 1:
            return images[1]
        if self.competition == COMPETITIONS.EUROLEAGUE or self.competition == COMPETITIONS.EUROCUP:
            return images

    def correct_color(self, bad_color):
        '''
            Method which find the nearest color to our list of colors self.colors from a color detected in a pixel of an image
            :param bad_color: Color which has not been found in our list of colours self.colors
            :return: return a color from our list of colors self.colors
        '''
        result = {}
        for k, v in self.colors.items():
            color = int(codecs.encode(k)[1:], 16)
            bc = int(codecs.encode(bad_color)[1:], 16)
            subs = abs(color - bc)
            result[k] = subs
        ordered = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
        return next(iter(ordered.keys()))

    def set_positions(self):
        '''Set the place in the field of each shoot'''
        list_of_colors = self.colors
        images = self.load_images()
        colors = {}
        for c in list_of_colors.keys():
            colors[c] = 0
        other_colors = {}
        self.errores = 0
        #print(f"Total lanzamientos: {len(self.df)}")
        for index, row in self.df.iterrows():
            image = self.select_image(images, row["team"])
            color = image.get_color(row["x"], row["y"])
            #print(f"Color que vamos a tratar:: color {color} - (x, y): {row['x'], row['y']}!!!")
            if color in list_of_colors:
                self.df.at[index, "position"] = list_of_colors[color]
                colors[color] = colors[color] + 1
                #print(f"Encontrado:: color {color} - (x, y): {row['x'], row['y']}!!!")
            else:
                #COLOR NOT FOUND
                gc = self.correct_color(color)
                self.df.at[index, "position"] = list_of_colors[gc]
                colors[gc] = colors[gc] + 1
                self.errores = self.errores + 1
                # if color in other_colors:
                #     other_colors[color] = other_colors[color] + 1
                # else:
                #     other_colors[color] = 1
        # print(f"colors: {colors}\n total_colors: {len(colors.keys())}")
        # for k, v in sorted(colors.items(), key=itemgetter(1), reverse=True):
        #     print (k, v)
        # print(f"other colors: {other_colors}\n total other colors: {len(other_colors.keys())}")
        # print(f"errores: {self.errores}")


    def get_all_colors(self):
        image = ShotChartImage(IMAGES.TEST_COLOUR_MAP)
        list_of_colors = self.colors
        colors = {}
        for c in list_of_colors.keys():
            colors[c] = 0
        other_colors = {}
        errores = 0
        for y in range(image.image.height):
            for x in range(image.image.width):
                color = image.get_color(x, y)
                if color in list_of_colors:
                    colors[color] = colors[color] + 1
                else:
                    #Color not found
                    gc = self.correct_color(color)
                    colors[gc] = colors[gc] + 1
                    errores = errores + 1
                    if color in other_colors:
                        other_colors[color] = other_colors[color] + 1
                    else:
                        other_colors[color] = 1
        print(f"Colors matched: {colors}\n colors matched: {len(colors.keys())}")
        # for k, v in sorted(colors.items(), key=itemgetter(1), reverse=True):
        #     print (k, v)
        print(f"Other colors: {other_colors})\ntotal other colors: {len(other_colors.keys())}")
        for k, v in sorted(other_colors.items(), key=itemgetter(1), reverse=True):
            print (k, v)
        print(f"errores: {errores}")
