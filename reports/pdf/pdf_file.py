from fpdf import FPDF
from constants import PDFK, COMPETITIONS, SEASONS, IMAGES
from pathlib import Path
import os
import abc
from PIL import Image
from decimal import Decimal
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.shots.player_shots import PlayerShots
from com.shotchart.images.shotchartimage import ShotChartImage
import locale
import datetime
from com.graphics.doublebar_chart_plot import MultiBarChatPlot


class PDFFile(object, metaclass=abc.ABCMeta):
    '''
        Constructor receive two parameters, a dictionary and an object with data
        params: {
            "type": "preGame",
            "competition": params["competition"]
            "destiny": params["destiny"],
            "home": params["home"],
            "away": params["away"],
            "date": params["date"],
            "home_team": home_data["name"],
            "away_team": away_data["name"],
            "home_url": home_data["url_name"],
            "away_url": away_data["url_name"]
        }
        data_pre_game is an object with these data:
            home_standard_stats
            away_standard_stats
            home_opps_standard_stats
            away_opps_standard_stats
            home_advanced_stats
            away_advanced_stats
            home_pt_ss
            away_pt_ss
            players_home_as
            players_away_as
    '''
    def __init__(self, params):
        self.pdf = self.pdf = FPDF('L', 'pt', 'A4')
        self.pdf.compress = True
        self.params = params
        self.fileName = None
        # if "month" not in params:
        #     print(f"Creo PDF {params['type']}: {params['home_team']} - {params['away_team']}")
        # else:
        #     locale.setlocale(locale.LC_TIME, "")
        #     d = datetime.date(params["year"], params["month"], 1)
        #     print(f"Creo PDF {params['type']} ({d.strftime('%B/%Y').capitalize()}): {params['home_team']}")

    def get_season(self, competition):
        '''Returns the id of a season'''
        if competition == COMPETITIONS.LF1:
            return SEASONS.LF1_SEASON
        if competition == COMPETITIONS.LF2:
            return SEASONS.LF2_SEASON
        if competition == COMPETITIONS.EUROLEAGUE:
            return SEASONS.EUROLEAGUE_SEASON
        if competition == COMPETITIONS.EUROCUP:
            return SEASONS.EUROCUP

    def create_page(self, title, number_page = True):
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.header(title)
        self.set_footer(number_page)

    def cover(self):
        self.pdf.add_page()
        self.set_title_cover()
        self.set_type_inform_cover()
        self.set_date_cover()
        self.set_footer(False)

    def set_date_cover(self):
        self.pdf.set_font('Arial', "", 14)
        date = "Fecha informe: " + self.params["date"]
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(date)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 + 72, date)

    def save_pdf(self, params):
        Path(PDFK.REPORT_ROUTES).mkdir(parents=True, exist_ok=True)
        #print("Existe? {}".format(os.path.exists(str(params["destiny"]))))
        if not os.path.exists(PDFK.REPORT_ROUTES + str(params["destiny"])):
            os.makedirs(PDFK.REPORT_ROUTES + str(params["destiny"]))
        if "home_url" in params and "away_url" in params:
            route_file = PDFK.REPORT_ROUTES + str(params["destiny"]) + "/" + params["type"] + "-" + \
                         params["home_url"] + ".vs." + params["away_url"] + ".pdf"
        else:
            team = params["home_url"] if "home_url" in params else params["away_url"]
            locale.setlocale(locale.LC_TIME, "")
            d = datetime.date(params["year"], params["month"], 1)
            month = d.strftime("%B")
            route_file = PDFK.REPORT_ROUTES + str(params["destiny"]) + "/" + month + "-" + \
                         team + ".pdf"

        self.fileName = route_file
        self.pdf.output(route_file)
        print(f"PDF guardado: {route_file}")

    @abc.abstractmethod
    def set_title_cover(self):
        raise NotImplementedError("No se ha implementado el método 'set_title_cover' por el usuario")

    def set_type_inform_cover(self):
        raise NotImplementedError("No se ha implementado el métido 'set_type_inform_cover' por el usuario")

    def header(self, title):
        # Select Arial bold 15
        self.pdf.set_font('Arial', 'B', 18)
        # Move to the right
        #self.pdf.cell(80)
        # Framed title
        self.pdf.cell(0, 25, title, "B: 1", 0, 'L')
        # Line break
        self.pdf.ln(20)

    @staticmethod
    def locale_format(d):
        '''Returns a number in spanish format'''
        return locale.format('%0.2f', d, grouping=True)

    def resize_image(self, file, new_width):
        img = Image.open(file)
        (width, height) = img.size
        percentage_size = round(Decimal(new_width*100/width), 2)
        new_height = round(Decimal(height*percentage_size/100), 0)
        #print(f"new_width: {new_width} new_height: {new_height}")
        return (int(new_width), int(new_height))

    def page_standard_stats(self, params, hss, ass):
        '''
            Method which writes the page of standard stats
            :param params: values of menu
            :param hss: Home standard stats from team
            :param ass: Away standard stats from team
        :return: 
        '''
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        away = params["away_team"]
        home = params["home_team"]
        # print(f"object1: {hss}")
        # print(f"object2: {ass}")
        away_ss = ass[0]
        home_ss = hss[0]
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro totales") + 5, 15, "Estadísticas de tiro totales", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2PC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2PI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3PC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3PI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TCC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TCI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TC%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TLC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TLI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PTOS", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(120)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["t2p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["t2p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["t3p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["t3p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["tc_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["tc_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["tl_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["tl_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["total_puntos"]), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(140)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(away_ss["t2p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["t2p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["t3p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["t3p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["tc_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["tc_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["tl_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["tl_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["total_puntos"]), 1, 0, "C", 0)
        #Estadísticas de tiro por partido
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(180)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro por partido") + 5, 15, "Estadísticas de tiro por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(205)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2PC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2PI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T2P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3PC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3PI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "T3P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TCC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TCI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TC%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TLC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TLI", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PTOS", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(225)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t2p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t2p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t3p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t3p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tc_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tc_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tl_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tl_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["total_puntos_pp"])), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(245)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t2p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t2p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t3p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t3p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tc_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tc_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tl_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tl_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["total_puntos_pp"])), 1, 0, "C", 0)
        #Estadísticas de rebotes
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(285)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de rebote totales y por partido") + 5, 15, "Estadísticas de rebote totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(310)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD/P", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO/P", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR/P", 1, 0, "C", 1)
        #Fila equipo rival
        self.pdf.set_y(330)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(home_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(home_ss["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(home_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(home_ss["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(home_ss["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(home_ss["total_rebs_pp"])), 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_y(350)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(away_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(away_ss["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(away_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(away_ss["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(away_ss["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(away_ss["total_rebs_pp"])), 1, 0, "C", 0)
        #Otras estadísticas
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(390)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales y por partido") + 5, 15, "Otras estadísticas totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(415)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BR", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BR/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BP/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TP/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FC/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FR", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FR/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "VAL.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "VAL./P", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(435)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["assists"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["assists_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["steals"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["steals_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["turnovers_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["block_shots_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["fouls_cm_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["fouls_rv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["efficience"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["efficience_pp"])), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(455)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(away_ss["assists"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["assists_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["steals"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["steals_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["turnovers_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["block_shots_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["fouls_cm_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["fouls_rv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["efficience"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["efficience_pp"])), 1, 0, "C", 0)

    def page_advanced_stats(self, params, data):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        away = params["away_team"]
        home = params["home_team"]
        away_ss = data.away_standard_stats[0]
        home_ss = data.home_standard_stats[0]
        away_as = data.away_advanced_stats[0]
        home_as = data.home_advanced_stats[0]
        #Calculo de % de lanzamientos
        poss = home_ss["tl_int"]*0.44 + home_ss["t2p_int"] + home_ss["t3p_int"] + home_ss["turnovers"]
        #poss = team_as["possessions"]
        home_2p = round(Decimal((home_ss["t2p_int"])/poss * 100), 2)
        home_3p = round(Decimal((home_ss["t3p_int"])/poss * 100), 2)
        home_tov = round(Decimal((home_ss["turnovers"])/poss * 100), 2)
        home_1p = round(Decimal((home_ss["tl_int"])/poss * 100), 2)
        poss = away_ss["tl_int"]*0.44 + away_ss["t2p_int"] + away_ss["t3p_int"] + away_ss["turnovers"]
        away_2p = round(Decimal((away_ss["t2p_int"])/poss * 100), 2)
        away_3p = round(Decimal((away_ss["t3p_int"])/poss * 100), 2)
        away_tov = round(Decimal((away_ss["turnovers"])/poss * 100), 2)
        away_1p = round(Decimal((away_ss["tl_int"])/poss * 100), 2)
        #Tabla 4 Factores
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("4 Factores") + 5, 15, "4 Factores", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 40, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_fill_color(225, 0, 0)
        self.pdf.cell(290, 20, "4 FACTORES DEFENSIVOS", 1, 0, "C", 1)
        self.pdf.set_fill_color(0, 0, 225)
        self.pdf.cell(280, 20, "4 FACTORES OFENSIVOS", 1, 0, "C", 1)
        self.pdf.set_xy(228, 120)
        self.pdf.set_fill_color(225, 0, 0)
        self.pdf.cell(70, 20, "Rival eTC%", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "Reb.Def.%", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "Rival BP%", 1, 0, "C", 1)
        self.pdf.cell(80, 20, "Rival TL Ratio", 1, 0, "C", 1)
        self.pdf.set_fill_color(0, 0, 225)
        self.pdf.cell(70, 20, "eTC%", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "Reb.Of.%", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "BP%", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "TL Ratio", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(140)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["rival_p_etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["p_reb_def"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["rival_p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(80, 20, self.locale_format(Decimal(home_as["rival_ratio_ft"])), 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["p_reb_of"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as["ratio_ft"])), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(160)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["rival_p_etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["p_reb_def"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["rival_p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(80, 20, self.locale_format(Decimal(away_as["rival_ratio_ft"])), 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["p_reb_of"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(away_as["ratio_ft"])), 1, 0, "C", 0)
        #Tabla Posesiones
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(205)
        self.pdf.cell(self.pdf.get_string_width("Posesiones") + 5, 15, "Posesiones", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(230)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "POS.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PACE", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PPP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PPI", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(250)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, self.locale_format(Decimal(home_as["possessions"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_as["possessions_x_minute"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["ppa"])), 1, 0, "C", 0)
         #Fila equipo visitante
        self.pdf.set_y(270)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, self.locale_format(Decimal(away_as["possessions"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_as["possessions_x_minute"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(away_ss["ppa"])), 1, 0, "C", 0)
        #Tabla Distribución de posesiones
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_xy(430, 205)
        self.pdf.cell(self.pdf.get_string_width("Distribución de posesiones") + 5, 15, "Distribución de posesiones", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_xy(430, 230)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "2P%", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "3P%", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "TL%", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "BP%", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_xy(430, 250)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(42, 20, self.locale_format(home_2p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(home_3p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(home_1p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(home_tov) + "%", 1, 0, "C", 0)
        #Fila equipo visitnte
        self.pdf.set_xy(430, 270)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(42, 20, self.locale_format(away_2p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(away_3p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(away_1p) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(away_tov) + "%", 1, 0, "C", 0)
        #Índices de eficiencia
        self.pdf.ln()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(315)
        self.pdf.cell(self.pdf.get_string_width("Índices de eficiencia") + 5, 15, "Índices de eficiencia", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(340)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "ORTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "DRTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "NRTG", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(360)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(home_as["ortg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(home_as["drtg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(home_as["nrtg"]), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(380)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(away_as["ortg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(away_as["drtg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(away_as["nrtg"]), 1, 0, "C", 0)
        #Tabla tiros
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_xy(430, 315)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro") + 5, 15, "Estadísticas de tiro", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_xy(430, 340)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "eTC%", 1, 0, "C", 1)
        self.pdf.cell(42, 20, "TS%", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_xy(430, 360)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(42, 20, self.locale_format(Decimal(home_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(Decimal(home_as["ts"])) + "%", 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_xy(430, 380)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(42, 20, self.locale_format(Decimal(away_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(Decimal(away_as["ts"])) + "%", 1, 0, "C", 0)
        #Tabla tiros
        self.pdf.ln()
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(425)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas") + 5, 15, "Otras estadísticas", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(450)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "AS/BP", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "BR/BP", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(470)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(Decimal(home_as["assists_x_turnovers"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(home_as["steals_x_turnovers"])), 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_y(490)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(Decimal(away_as["assists_x_turnovers"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(away_as["steals_x_turnovers"])), 1, 0, "C", 0)

    def page_team_graphics_1(self, hss, ass):
        '''
            Draw graphics: distribution of possession and distribution of points
            :param hss: Home standard stats
            :param ass: Away standardstats
        :return:
        '''
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = hss[0]
        away_team = ass[0]
        # home_as = self.dpg.home_advanced_stats[0]
        # away_as = self.dpg.away_advanced_stats[0]
        poss = home_team["tl_int"]*0.44 + home_team["t2p_int"] + home_team["t3p_int"] + home_team["turnovers"]
        home_2p = round(Decimal((home_team["t2p_int"])/poss * 100), 2)
        home_3p = round(Decimal((home_team["t3p_int"])/poss * 100), 2)
        home_tov = round(Decimal((home_team["turnovers"])/poss * 100), 2)
        home_1p = round(Decimal((home_team["tl_int"])/poss * 100), 2)
        poss = away_team["tl_int"]*0.44 + away_team["t2p_int"] + away_team["t3p_int"] + away_team["turnovers"]
        away_2p = round(Decimal((away_team["t2p_int"])/poss * 100), 2)
        away_3p = round(Decimal((away_team["t3p_int"])/poss * 100), 2)
        away_tov = round(Decimal((away_team["turnovers"])/poss * 100), 2)
        away_1p = round(Decimal((away_team["tl_int"])/poss * 100), 2)
        self.pdf.set_y(75)
        legends = [home_team["abrev"], away_team["abrev"]]
        labels = ["T2P%", "T3P%", "TL%", "BP%"]
        values = []
        values.append([home_2p, home_3p, home_1p, home_tov])
        values.append([away_2p, away_3p, away_1p, away_tov])
        file = str(self.params["home"]) + "." + str(self.params["away"]) + ".graphic1" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Distribución de posesiones", "Porcentaje")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [home_team["abrev"], away_team["abrev"]]
        labels = ["T2P", "T3P", "TL"]
        home_t1p = home_team["p_tl_puntos"]
        home_t2p = home_team["p_t2p_puntos"]
        home_t3p = home_team["p_t3p_puntos"]
        away_t1p = away_team["p_tl_puntos"]
        away_t2p = away_team["p_t2p_puntos"]
        away_t3p = away_team["p_t3p_puntos"]
        values = [[home_t2p, home_t3p, home_t1p], [away_t2p, away_t3p, away_t1p]]
        file = str(self.params["home"]) + "." + str(self.params["away"]) + ".graphic2" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Distribución de puntos", "Porcentaje")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)

    def page_team_graphics_2(self, hss, ass, has, aas):
        '''

            :param hss: Home standard stats
            :param ass: Away standard stats
            :param has: Home advanced stats
            :param aas: Away advanced stats
        :return:
        '''
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = hss[0]
        away_team = ass[0]
        home_as = has[0]
        away_as = aas[0]
        self.pdf.set_y(75)
        legends = [home_team["abrev"], away_team["abrev"]]
        labels = ["Pace", "PPI", "PPP"]
        values = []
        values.append([home_as["possessions_x_minute"], home_team["ppa"], home_team["pointsbyposs"]])
        values.append([away_as["possessions_x_minute"], away_team["ppa"], away_team["pointsbyposs"]])
        file = str(self.params["home"]) + "." + str(self.params["away"]) + ".graphic3" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Eficiencia", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [home_team["abrev"], away_team["abrev"]]
        labels = ["RD/P", "RO/P", "TR/P"]
        values = [[home_team["reb_def_pp"], home_team["reb_of_pp"], home_team["total_rebs_pp"]], [away_team["reb_def_pp"], away_team["reb_of_pp"], away_team["total_rebs_pp"]]]
        file = str(self.params["home"]) + "." + str(self.params["away"]) + ".graphic4" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Rebotes por partido", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)


    def set_advertencia(self, tci, data, errores):
        '''
        :param tci:         Attempted shoots
        :param data:        DataFrame with shoots
        :param errores:     Number of shoots not located correctly in any sector
        :return:
        '''
        #Advertencia
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_xy(535, 65)
        self.pdf.cell(self.pdf.get_string_width("Advertencia"), 10, "Advertencia", fill=(0, 0, 0), ln=1)
        self.pdf.set_xy(535, 85)
        self.pdf.set_font("Arial", "", 12)
        txt = "Se ha detectado una incongruencia entre los tiros lanzados por un equipo o jugadora que aparecen informados en la estadística y los lanzamientos que hay registrados como tales."
        self.pdf.multi_cell(275, 15, txt, 0, "J", 0)
        self.pdf.ln()
        self.pdf.set_x(535)
        self.pdf.set_font("Arial", "", 12)
        self.pdf.multi_cell(275, 15, f"Lanzamientos realizados: {tci}", 0, "J", fill=(0, 0, 0))
        self.pdf.set_x(535)
        self.pdf.multi_cell(275, 15, f"Lanzamientos tratados: {len(data)}", 0, "J", fill=(0, 0, 0))

    def set_footer(self, number_page):
        # Position at 1.5 cm from bottom
        self.pdf.set_y(-70)
        # Arial italic 8
        self.pdf.set_font('Arial', 'I', 12)
        # Page number
        if number_page:
            self.pdf.cell(0, 10, " - " + str(self.pdf.page_no()) + "/{nb} - ", 0, 0, "C")
        self.pdf.cell(0, 10, 'www.basketmetrics.com', 0, 0, 'R')
        #self.pdf.cell(PDFK.A4_WIDTH, 10, "www.basketmetrics.com", border = 1, align = "R")

    def shot_chart_player(self, id_team, id_player_team, tci):
        #get stats of shots from opponent team and players
        opp = self.params["away"] if self.params["destiny"] == self.params["home"] else self.params["home"]
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(opp, self.params["competition"])
        #ps = PlayerShots(ts.get_player_data(id_player_team), ts.id_team_club, ts.competition)
        #ps = PlayerShots(self.params)
        #self.set_advertencia(tci, ps.df, ps.errores)
        self.set_advertencia(tci, ts.get_player_data(id_player_team), 0)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        image.set_data_over_image(ts.get_player_data(id_player_team), ss.df)
        name = f"{id_team}-{id_player_team}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #Tabla Estadísticas de tiro
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        #self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def shot_chart_team(self, tci):
        #get stats from shots from opponent team
        opp = self.params["away"] if self.params["destiny"] == self.params["home"] else self.params["home"]
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(opp, self.params["competition"])
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, ts.df, ts.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(ts.df, ss.df)
        #Save image
        name = "test.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def page_glosario_1(self):
        self.pdf.set_y(65)
        self.set_lci_glosario("AS:", "Asistencias")
        self.set_lci_glosario("AS Ratio:", "De cada posesión cuales de ellas terminan con una asistencia")
        self.set_lci_glosario("AS%:", "Porcentaje de asistencias")
        self.set_lci_glosario("AS/P:", "Asistencias por partido")
        self.set_lci_glosario("AS/BP: ", "Número de asistencias dadas por balón perdido")
        self.set_lci_glosario("BP: ", "Balones Perdidos")
        self.set_lci_glosario("BP%: ", "De todas las posesiones jugadas, porcentaje de balones perdidos")
        self.set_lci_glosario("BP/P: ", "Balones perdidos por partido")
        self.set_lci_glosario("BR: ", "Balones recuperados")
        self.set_lci_glosario("BR%: ", "Porcentaje de balones recuperados")
        self.set_lci_glosario("BR/BP: ", "Número de balones recuperados por cada balón perdido")
        self.set_lci_glosario("BR/P: ", "Balones recuperados por partido")
        self.set_lci_glosario("DRE: ", "Daily RAPM (Regularized Adjusted Plus/Minus) Estimate. Equivalente al +/- pero mucho más restrictivo")
        self.set_lci_glosario("DRTG: ", "Defensive Rating o Ratio Defensivo o Índice defensivo. Número de puntos recibidos por un equipo o una jugadora en 100 posesiones")
        self.set_lci_glosario("eTC%: ", "Eficiencia en tiros de campos (Effective Field Goal Percentage). Esta estadística recoge el acierto en el tiro dándole una mayor importancia a los triples respecto a los tiros de dos puntos")
        self.set_lci_glosario("FC: ", "Faltas cometidas")
        self.set_lci_glosario("FC/P: ", "Faltas cometidas por partido")
        self.set_lci_glosario("FR: ", "Faltas recibidas")
        self.set_lci_glosario("FR/P: ", "Faltas recibidas por partido")
        self.set_lci_glosario("GS: ", "Game Score. Métrica equivalente y más exisgente que la valoración de una jugadora")
        self.pdf.set_xy(425, 65)
        self.set_lcd_glosario("NRTG: ", "Diferencia entre ORTG y DRTG")
        self.set_lcd_glosario("ORTG: ", "Offensive Rating o Ratio Ofensivo o Índice ofensivo. Número de puntos anotados por un equipo o una juadora en 100 posesiones")
        self.set_lcd_glosario("PACE: ", "Ritmo de partido. Número de posesiones por minuto.")
        self.set_lcd_glosario("PJ: ", "Partidos jugados.")
        self.set_lcd_glosario("POS: ", "Posesiones")
        self.set_lcd_glosario("PPI: ", "Puntos anotados por intento")
        self.set_lcd_glosario("PPP: ", "Puntos anotados por posesión")
        self.set_lcd_glosario("PTOS: ", "Puntos anotados")
        self.set_lcd_glosario("RD: ", "Rebote defensivos")
        self.set_lcd_glosario("RD/P: ", "Rebote defensivos por partido")
        self.set_lcd_glosario("Reb. Def. %: ", "Porcentaje de rebotes defensivos")
        self.set_lcd_glosario("Reb. Of. %: ", "Porcentaje de rebotes ofensivos")
        self.set_lcd_glosario("RO: ", "Rebote ofensivos")
        self.set_lcd_glosario("RO/P: ", "Rebote ofensivos por partido")
        self.set_lcd_glosario("Rival BP%: ", "Porcentaje de balones perdidos por el rival")
        self.set_lcd_glosario("Rival eTC%: ", "Porcentaje de efictividad de tiro del rival")
        self.set_lcd_glosario("Rival TL Ratio: ", "De cada punto del equipo rival, cuánto proviene de los tiros libres")
        self.set_lcd_glosario("T2PC: ", "Tiros de dos puntos convertidos")
        self.set_lcd_glosario("T2PI: ", "Tiros de dos puntos intentados")
        self.set_lcd_glosario("T2P%: ", "Porcentaje de tiros de dos puntos")


    def page_glosario_2(self):
        self.pdf.set_y(65)
        self.set_lci_glosario("T3PC: ", "Tiros de tres puntos convertidos")
        self.set_lci_glosario("T3PI: ", "Tiros de tres puntos intentados")
        self.set_lci_glosario("T3P%: ", "Porcentaje de tiros de tres puntos")
        self.set_lci_glosario("TCC: ", "Tiros de campo convertidos")
        self.set_lci_glosario("TCI: ", "Tiros de campo intentados")
        self.set_lci_glosario("TC%: ", "Porcentaje de tiros de campo")
        self.set_lci_glosario("TLC: ", "Tiros libres convertidos")
        self.set_lci_glosario("TLI: ", "Tiros libre intentados")
        self.set_lci_glosario("TL%: ", "Porcentaje de tiros libres")
        self.set_lci_glosario("TL Ratio:", "De cada punto del equipo, cuánto proviene de los tiros libres")
        self.set_lci_glosario("TP:", "Tapones")
        self.set_lci_glosario("TP/P: ", "Tapones por partido")
        self.set_lci_glosario("TR: ", "Total rebotes")
        self.set_lci_glosario("TR%: ", "Porcentaje del total de rebotes")
        self.set_lci_glosario("T/R: ", "Total rebotes por partido")
        self.set_lci_glosario("TS%: ", "True shooting. Se mide la eficiencia de tiro de una jugadora, teniendo en cuenta los tiros de dos, de tres y tiros libres")
        self.set_lci_glosario("USG%: ", "Número de posesiones finalizadas por una jugadora. Uso de la jugadora en ataque")
        self.set_lci_glosario("VAL: ", "Valoración")
        self.set_lci_glosario("VAL/P: ", "Valoración por partido")

    def set_lci_glosario(self, stat, texto):
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(self.pdf.get_string_width(stat), 10, stat)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(350 - self.pdf.get_string_width(stat), 10, texto, 0, "J", 0)
        self.pdf.ln()

    def set_lcd_glosario(self, stat, texto):
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(self.pdf.get_string_width(stat), 10, stat)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(350 - self.pdf.get_string_width(stat), 10, texto, 0, "J", 0)
        self.pdf.ln()
        self.pdf.set_x(425)
