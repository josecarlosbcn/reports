from reports.pdf.pdf_file import PDFFile
from constants import PDFK
from pathlib import Path
import os
import locale
import datetime
from decimal import Decimal
from constants import COMPETITIONS, IMAGES
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.player_shots import PlayerShots
from com.shotchart.images.shotchartimage import ShotChartImage
from com.graphics.doublebar_chart_plot import MultiBarChatPlot
from com.graphics.bar_chart_plot import BarChartPlot


class PDFMonthly(PDFFile):
    def __init__(self, params, data_monthly):
        '''
        :param params: Contains the values of:
            - type:  "monthly",
            - destiny: id of the team who will receive the report
            - competition: Constant value which represents a competition
            - month: Mes del informe
            - year: Año del informe
            - home_team: Nombre del equipo
            - home_url: Nombre del equipo para nombres de ficheros
        :param data_monthly:
        '''
        super().__init__(params)
        self.dm = data_monthly
        #print(f"params: {params}")
        #print(f"hss: {self.dm.team_standard_stats.keys()}")
        #Creamos página principal
        self.cover()
        #Creamos página comparativa de estadísticas
        print("PDFMonthly:: Creando página comparativa de estadísticas estándar")
        self.create_page(f"{params['home_team']}: Estadística Estándard")
        self.page_standard_stats(params)
        print("PDFMonthly:: Creando página comparativa de estadísticas avanzadas")
        self.create_page(f"{params['home_team']}: Estadística Avanzada")
        self.page_advanced_stats(params)
        #Creamos carta de tiro del equipo local
        print("PDFMonthly:: Creando carta de tiro de los equipos")
        self.create_page(f"Carta de tiro: {params['home_team']}")
        team_ss = self.dm.team_standard_stats
        self.shot_chart_team(team_ss['tc_int'], self.params["destiny"])
        #Creamos carta de tiro de los rivales
        self.create_page(f"Carta de tiro: Rivales")
        rivales_ss = self.dm.opps_standard_stats
        self.shot_chart_opp(rivales_ss['tc_int'], self.params["destiny"])
        #Gráficas comparativas
        print("PDFMonthly:: Creando página con gráficas comparativas entre equipos")
        self.create_page("Gráficas comparativas entre equipos 1/2")
        self.page_team_graphics_1()
        self.create_page("Gráficas comparativas entre equipos 2/2")
        self.page_team_graphics_2()
        #Estadísticas de jugadoras y cartas de tiro de jugadoras
        print("PDFMonthly:: Creando páginas de estadísticas y carta de tiro de jugadoras")
        self.players_page(params)
        #Gráficas de jugadoras
        print("PDFMonthly:: Creando páginas de gráficas comparativas entre jugadoras")
        self.create_page("Gráficas comparativas entre jugadoras")
        self.page_player_graphics()
        #Glosario
        print("PDFMonthly:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        print("PDFMonthly:: Vamos a guardar PDF")
        self.save_pdf(params)

    def page_standard_stats(self, params):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        away = "Rivales"
        home = params["home_team"]
        # print(f"object: {self.dpg.away_standard_stats}")
        home_ss = self.dm.team_standard_stats
        rivales_ss = self.dm.opps_standard_stats
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro totales") + 5, 15, "Estadísticas de tiro totales", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
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
        # self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["games"]), 1, 0, "C", 0)
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
        #Fila equipos rivales
        self.pdf.set_y(140)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(rivales_ss["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["t2p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["t2p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["t3p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["t3p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["tc_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["tc_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["tl_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["tl_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["total_puntos"]), 1, 0, "C", 0)
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
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
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
        self.pdf.cell(40, 20, str(home_ss["games"]), 1, 0, "C", 0)
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
        #Fila equipos rivales
        self.pdf.set_y(245)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(int(rivales_ss["games"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t2p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t2p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t3p_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t3p_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tc_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tc_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tl_conv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tl_int_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["total_puntos_pp"])), 1, 0, "C", 0)
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
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "RD/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "RO/P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TR", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TR/P", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(330)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["total_rebs_pp"])), 1, 0, "C", 0)
        #Fila equipo rival
        self.pdf.set_y(350)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(rivales_ss["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["total_rebs_pp"])), 1, 0, "C", 0)
        #Otras estadísticas
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(390)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales y por partido") + 5, 15, "Otras estadísticas totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(415)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(180, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
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
        self.pdf.cell(180, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["games"]), 1, 0, "C", 0)
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
        #Fila equipos rivales
        self.pdf.set_y(455)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(180, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(rivales_ss["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["assists"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["assists_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["steals"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["steals_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["turnovers_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["block_shots_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["fouls_cm_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["fouls_rv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(rivales_ss["efficience"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(rivales_ss["efficience_pp"])), 1, 0, "C", 0)

    def page_advanced_stats(self, params):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        home = params["home_team"]
        away = "Rivales"
        home_ss = self.dm.team_standard_stats
        home_as = self.dm.team_advanced_stats
        opp_ss = self.dm.opps_standard_stats
        opp_as = self.dm.opp_advanced_stats
        #Calculo de % de lanzamientos
        poss = Decimal(home_ss["tl_int"])*Decimal(0.44) + home_ss["t2p_int"] + home_ss["t3p_int"] + home_ss["turnovers"]
        #poss = team_as["possessions"]
        home_2p = round(Decimal((home_ss["t2p_int"])/poss * 100), 2)
        home_3p = round(Decimal((home_ss["t3p_int"])/poss * 100), 2)
        home_tov = round(Decimal((home_ss["turnovers"])/poss * 100), 2)
        home_1p = round(Decimal((home_ss["tl_int"])/poss * 100), 2)
        poss = Decimal(opp_ss["tl_int"])*Decimal(0.44) + opp_ss["t2p_int"] + opp_ss["t3p_int"] + opp_ss["turnovers"]
        away_2p = round(Decimal((opp_ss["t2p_int"])/poss * 100), 2)
        away_3p = round(Decimal((opp_ss["t3p_int"])/poss * 100), 2)
        away_tov = round(Decimal((opp_ss["turnovers"])/poss * 100), 2)
        away_1p = round(Decimal((opp_ss["tl_int"])/poss * 100), 2)
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
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_rival_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_percentage_reb_def())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_rival_percentage_turnovers())) + "%", 1, 0, "C", 0)
        self.pdf.cell(80, 20, self.locale_format(Decimal(home_as.get_rival_ratio_ft())), 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_percentage_reb_of())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_percentage_turnovers())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(home_as.get_ratio_ft())), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(160)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, "Rivales", 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_rival_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_percentage_reb_def())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_rival_percentage_turnovers())) + "%", 1, 0, "C", 0)
        self.pdf.cell(80, 20, self.locale_format(Decimal(opp_as.get_rival_ratio_ft())), 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_percentage_reb_of())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_percentage_turnovers())) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as.get_ratio_ft())), 1, 0, "C", 0)
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
        self.pdf.cell(60, 20, self.locale_format(Decimal(home_as.get_possessions())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_as.get_possession_time())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(home_ss["ppa"])), 1, 0, "C", 0)
         #Fila equipo rival
        self.pdf.set_y(270)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away, 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, self.locale_format(Decimal(opp_as.get_possessions())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(opp_as.get_possession_time())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(opp_ss["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(opp_ss["ppa"])), 1, 0, "C", 0)
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
        self.pdf.cell(45, 20, self.locale_format(home_as.get_ortg()), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(home_as.get_drtg()), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(home_as.get_nrtg()), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(380)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(opp_as.get_ortg()), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(opp_as.get_drtg()), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(opp_as.get_nrtg()), 1, 0, "C", 0)
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
        self.pdf.cell(42, 20, self.locale_format(Decimal(home_as.get_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(Decimal(home_as.get_ts())) + "%", 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_xy(430, 380)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(42, 20, self.locale_format(Decimal(opp_as.get_etc())) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(Decimal(opp_as.get_ts())) + "%", 1, 0, "C", 0)
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
        self.pdf.cell(45, 20, self.locale_format(Decimal(home_as.get_ratio_assists_turnovers())), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(home_as.get_ratio_steals_turnovers())), 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_y(490)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(Decimal(opp_as.get_ratio_assists_turnovers())), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(opp_as.get_ratio_steals_turnovers())), 1, 0, "C", 0)

    def set_date_cover(self):
        pass

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.set_text_color(4, 52, 116)
        team = self.params["home_team"] if "home_team" in self.params else self.params["away_team"]
        locale.setlocale(locale.LC_TIME, "")
        d = datetime.date(self.params["year"], self.params["month"], 1)
        date = d.strftime("%B / %Y").capitalize()
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["home_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, team)
        self.pdf.set_font('Arial', '', 26)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(date)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, date)

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Informe mensual")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 + 50, "Informe mensual")

    def shot_chart_team(self, tci, id_team = None):
        #get stats from shots from opponent team
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(id_team, self.params["competition"])
        ts.get_shots_from_month(id_team, self.params["competition"], self.params["month"], self.params["year"])
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, ts.df, ts.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(ts.df, ss.df)
        #Save image
        name = f"team-{id_team}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def shot_chart_opp(self, tci, id_team = None):
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(id_team, self.params["competition"])
        ts.get_opp_shots_from_month(id_team, self.params["competition"], self.params["month"], self.params["year"])
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, ts.df, ts.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(ts.df, ss.df)
        #Save image
        name = f"opp-{id_team}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def page_team_graphics_1(self):
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = self.dm.team_standard_stats
        away_team = self.dm.opps_standard_stats
        abrev = self.dm.abrev
        home_as = self.dm.team_advanced_stats
        away_as = self.dm.opp_advanced_stats
        poss = Decimal(home_team["tl_int"])*Decimal(0.44) + home_team["t2p_int"] + home_team["t3p_int"] + home_team["turnovers"]
        home_2p = round(Decimal((home_team["t2p_int"])/poss * 100), 2)
        home_3p = round(Decimal((home_team["t3p_int"])/poss * 100), 2)
        home_tov = round(Decimal((home_team["turnovers"])/poss * 100), 2)
        home_1p = round(Decimal((home_team["tl_int"])/poss * 100), 2)
        poss = Decimal(away_team["tl_int"])*Decimal(0.44) + away_team["t2p_int"] + away_team["t3p_int"] + away_team["turnovers"]
        away_2p = round(Decimal((away_team["t2p_int"])/poss * 100), 2)
        away_3p = round(Decimal((away_team["t3p_int"])/poss * 100), 2)
        away_tov = round(Decimal((away_team["turnovers"])/poss * 100), 2)
        away_1p = round(Decimal((away_team["tl_int"])/poss * 100), 2)
        self.pdf.set_y(75)
        legends = [abrev, "Rivales"]
        labels = ["T2P", "T3P", "TL", "BP"]
        values = []
        values.append([home_2p, home_3p, home_1p, home_tov])
        values.append([away_2p, away_3p, away_1p, away_tov])
        file = str(self.params["destiny"]) + ".graphic1" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Distribución de posesiones", "Porcentaje")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [abrev, "Rivales"]
        labels = ["T2P", "T3P", "TL"]
        home_t1p = home_team["p_tl_puntos"]
        home_t2p = home_team["p_t2p_puntos"]
        home_t3p = home_team["p_t3p_puntos"]
        away_t1p = away_team["p_tl_puntos"]
        away_t2p = away_team["p_t2p_puntos"]
        away_t3p = away_team["p_t3p_puntos"]
        values = [[home_t2p, home_t3p, home_t1p], [away_t2p, away_t3p, away_t1p]]
        file = str(self.params["destiny"]) + ".graphic2" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Distribución de puntos", "Porcentaje")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)

    def page_team_graphics_2(self):
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = self.dm.team_standard_stats
        away_team = self.dm.opps_standard_stats
        home_as = self.dm.team_advanced_stats
        away_as = self.dm.opp_advanced_stats
        abrev = self.dm.abrev
        self.pdf.set_y(75)
        legends = [abrev, "Rivales"]
        labels = ["Pace", "PPI", "PPP"]
        values = []
        values.append([home_as.get_possession_time(), home_team["ppa"], home_team["pointsbyposs"]])
        values.append([away_as.get_possession_time(), away_team["ppa"], away_team["pointsbyposs"]])
        file = str(self.params["destiny"]) + ".graphic3" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Eficiencia", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [abrev, "Rivales"]
        labels = ["RD/P", "RO/P", "TR/P"]
        values = [[home_team["reb_def_pp"], home_team["reb_of_pp"], home_team["total_rebs_pp"]], [away_team["reb_def_pp"], away_team["reb_of_pp"], away_team["total_rebs_pp"]]]
        file = str(self.params["destiny"]) + ".graphic4" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Rebotes por partido", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)

    def players_page(self, params):
        pss = self.dm.players_team_ss
        pas = self.dm.players_team_as
        id_team = params["destiny"]
        if len(pss) != len(pas):
            raise Exception("PDFPreGame::players_page: El número de jugadoras en las estadísticas estándard no coincide con las avanzadas")
        for i in range(len(pss)):
            #print(f"Estadisticas estándar de {pss[i]['name']}, y estadisticas avanzadas de {pas[i]['name']}")
            locale.setlocale(locale.LC_TIME, "")
            d = datetime.date(self.params["year"], self.params["month"], 1)
            self.create_page(f"Estadísticas ({d.strftime('%B/%Y').capitalize()}): {pss[i]['name'].title()}")
            self.players_page_stats(pss[i], pas[i])
            if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.EUROLEAGUE \
                or params["competition"] == COMPETITIONS.EUROCUP:
                self.create_page(f"Carta de tiro ({d.strftime('%B/%Y').capitalize()}): {pss[i]['name'].title()}")
                print(f"\tGenerating shotchart of player: {pss[i]['name']}")
                self.shot_chart_player(id_team, pss[i]["id"], pss[i]["tc_int"])

    def players_page_stats(self, stats, adv):
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro totales") + 5, 15, "Estadísticas de tiro totales", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
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
        #Fila estadísticas
        self.pdf.set_font("Arial", "", 10)
        self.pdf.set_y(120)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["t2p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["t2p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["t3p_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["t3p_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tc_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tc_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tc_percentage"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tl_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tl_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tl_percentage"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["total_puntos"]), 1, 0, "C", 0)
        #Tabla Estadísticas de distribución de tiros
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_xy(640, 75)
        self.pdf.cell(self.pdf.get_string_width("Distribución de puntos") + 5, 15, "Distribución de puntos", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_xy(640, 100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "2P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "3P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_font("Arial", "", 10)
        self.pdf.set_xy(640, 120)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t2p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t3p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_tl_puntos"])) + "%", 1, 0, "C", 0)
        #Tabla Estadísticas de distribución de tiros por partido
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(155)
        self.pdf.cell(self.pdf.get_string_width("Distribución de tiros por partido") + 5, 15, "Distribución de tiros por partido", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(180)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
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
        #Fila estadísticas
        self.pdf.set_font("Arial", "", 10)
        self.pdf.set_y(200)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, self.locale_format(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["t2p_conv_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["t2p_int_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t2p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["t3p_conv_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["t3p_int_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t3p_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["tc_conv_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["tc_int_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tc_percentage"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["tl_conv_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["tl_int_pp"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tl_percentage"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(stats["total_puntos_pp"]), 1, 0, "C", 0)
        #Estadísticas de tiro por partido
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(240)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de rebote") + 5, 15, "Estadísticas de rebote", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(265)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(60, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD/P", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO/P", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR/P", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD%", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO%", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(285)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["total_rebs_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv.get_total_reb_def_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv.get_total_reb_of_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv.get_total_reb_percentage())) + "%", 1, 0, "C", 0)
        #Eficiencia
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(320)
        self.pdf.cell(self.pdf.get_string_width("Eficiencia") + 5, 15, "Eficiencia", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(345)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(45, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "PPP", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "PPI", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "USG%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "eTC%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "TS%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "ORTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "DRTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "NRTG", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(365)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(stats["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(stats["ppa"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_usg_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_effective_field_goal_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_ts_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_offensive_ratio())), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_defensive_ratio())), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv.get_net_ratio())), 1, 0, "C", 0)
        #Otras estadísticas
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(400)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales y por partido") + 5, 15, "Otras estadísticas totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(425)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(35, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "AS", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "AS/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BR", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BR/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BP", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BP/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "TP", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "TP/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FC", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FC/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FR", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FR/P", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "VAL.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "VAL./P", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "GS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "DRE", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS/BP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS.Rat.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BR%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(445)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(35, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["assists"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["assists_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["steals"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["steals_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["turnovers_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["block_shots_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["fouls_cm_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, self.locale_format(Decimal(stats["fouls_rv_pp"])), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["efficience"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["efficience_pp"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_game_score())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_dre())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_assists_percentage())) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_assists_per_turnover())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_assists_ratio())), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv.get_steals_percentage())) + "%", 1, 0, "C", 0)

    def shot_chart_player(self, id_team, id_player_team, tci):
        #get stats of shots from opponent team and players
        team = self.params["destiny"]
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(team, self.params["competition"])
        ts.get_shots_from_month(id_team, self.params["competition"], self.params["month"], self.params["year"])
        # ps = PlayerShots(ts.get_player_data(id_player_team), ts.id_team_club, ts.competition)
        # self.set_advertencia(tci, ps.df, ps.errores)
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

    def page_player_graphics(self):
        self.pdf.set_font("Arial", "B", 12)
        players = self.dm.players_team_ss
        total_points = self.dm.team_standard_stats["total_puntos"]
        labels = [player["name"] for player in players]
        values = [round(Decimal(player["total_puntos"]/total_points*100), 2) for player in players]
        file = str(self.params["destiny"]) + ".player.graphic.1" + IMAGES.EXTENSION
        barchart = BarChartPlot(labels, values, file, "Distribución de puntos por jugadora", "Porcentaje")
        barchart.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 550)
        self.pdf.set_xy(PDFK.LANDSCAPE_A4_WIDTH/2 - width/2, 65)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
