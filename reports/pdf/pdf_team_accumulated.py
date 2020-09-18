from reports.pdf.pdf_file import PDFFile
import datetime, os, locale, math
from datetime import datetime
from pathlib import Path
from constants import PDFK, IMAGES
from decimal import Decimal
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.images.shotchartimage import ShotChartImage
from com.shotchart.shots.accumulated_team_shots import AccumulatedTeamShots
from com.shotchart.shots.accumulated_opp_shots import AccumulatedOppShots
from com.graphics.doublebar_chart_plot import MultiBarChatPlot
from com.graphics.bar_chart_plot import BarChartPlot


class PDFTeamAccumulated(PDFFile):
    def __init__(self, params, data_accumulated):
        '''
        :param params: Contains the values of:
            - type:  "accumulated",
            - destiny: id of the team who will receive the report
            - competition: Constant value which represents a competition
            - team_name: Nombre del equipo
            - team_url: Nombre del equipo para nombres de ficheros
            - date: Fecha de generación del documento
        :param data_monthly:
        '''
        super().__init__(params)
        self.data = data_accumulated
        print("PDFAccumulated:: Creamos PDF")
        self.cover()
        #Creamos páginas con listado de partidos
        print("----PDFAccumulated:: Creamos páginas con listado de partidos")
        self.page_list_games()
        print("----PDFAccumulated:: Creamos página comparativa con estadísticas estándard")
        self.create_page(f"{params['team_name']}: Estadística Estándard")
        self.page_standard_stats(params)
        print("----PDFAccumuladted:: Creamos página comparativa de estadísticas avanzadas")
        self.create_page(f"{params['team_name']}: Estadística Avanzada")
        self.page_advanced_stats(params)
        self.create_page(f"Carta de tiro: {params['team_name']}")
        self.shot_chart_team(self.data.tss['tc_int'])
        self.create_page(f"Carta de tiro: Rivales")
        self.shot_chart_opp_team(self.data.oss['tc_int'])
        print("----PDFAccumuladted:: Creando página con gráficas comparativas entre equipos")
        self.create_page("Gráficas comparativas entre equipos 1/2")
        self.page_team_graphics_1()
        self.create_page("Gráficas comparativas entre equipos 2/2")
        self.page_team_graphics_2()
        print("----PDFAccumulated:: Creando página con gráfica comparativa entre jugadoras")
        self.create_page("Gráfica comparativa entre jugadoras")
        self.page_player_graphics()
        #Glosario
        print("PDFPreGame:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        print("PDFAccumulated:: Vamos a guardar PDF")
        self.save_pdf(params)

    def set_date_cover(self):
        pass

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.set_text_color(4, 52, 116)
        team = self.params["team_name"]
        date = self.params["date"]
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(team)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, team)
        self.pdf.set_font('Arial', '', 26)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(date)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, date)

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Estadísticas acumuladas")/2, PDFK.LANDSCAPE_A4_HEIGHT/2, "Estadísticas acumuladas")

    def set_bold(self, row):
        '''We define if the text is bold or not if the team plays at home or away. If it's plays at home the text is bold if it's away the text is not in bold'''
        if row["local"] == 1:   #Equipo local
            self.pdf.set_font("Arial", "B", 10)
        else:
            self.pdf.set_font("Arial", "", 10)

    def set_color(self, row):
        '''We set color of text depend of if the team has won the game or not'''
        if row["local"] == 1:
            if row["home_score"] > row["away_score"]:
                #self.pdf.set_text_color(23, 36, 14) #win color
                self.pdf.set_text_color(0, 125, 0)
            else:
                #self.pdf.set_text_color(88, 10, 24) #lose color
                self.pdf.set_text_color(225, 0, 0)
        else:
            if row["home_score"] > row["away_score"]:
                self.pdf.set_text_color(225, 0, 0)
            else:
                self.pdf.set_text_color(0, 125, 0)

    def set_advice(self):
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(125, 20, "Nota: En negrita, el equipo juega como local. En verde, victoria, en rojo, derrota.", 0, 0, "L", 0)

    def save_pdf(self, params):
        Path(PDFK.REPORT_ROUTES).mkdir(parents=True, exist_ok=True)
        team = params["team_url"]
        locale.setlocale(locale.LC_TIME, "")
        route_file = PDFK.REPORT_ROUTES + str(params["destiny"]) + "/"  + "accumulated-" + \
                     team + ".pdf"
        self.fileName = route_file
        self.pdf.output(route_file)
        print(f"PDF guardado: {route_file}")

    def header_list_games(self, y):
        '''Header of list of games for each page'''
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(y)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(60, 20, "Fecha", 1, 0, "C", 1)
        self.pdf.cell(105, 20, "Competición", 1, 0, "C", 1)
        self.pdf.cell(125, 20, "Rival", 1, 0, "C", 1)
        self.pdf.cell(55, 20, "Resultado", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "T2P", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "T3P", 1, 0, "C", 1)
        self.pdf.cell(70, 20, "TL", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "TR", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "AS", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "RB", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "BP", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "TP", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "FC", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "FR", 1, 0, "C", 1)
        self.pdf.cell(23, 20, "VAL", 1, 0, "C", 1)

    def row_game(self, row, y):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        self.set_color(row)
        self.set_bold(row)
        self.pdf.set_y(y)
        self.pdf.cell(60, 20, row['date_game'].strftime("%d/%m/%Y"), 1, 0, "L", 0)
        self.pdf.cell(105, 20, row['competition'] if len(row['competition']) <= 20 else row['competition'][:18] + "...", 1, 0, "L", 0)
        rival = row["home_team"] if row["local"] == 0 else row["away_team"]
        self.pdf.cell(125, 20, rival if len(rival) <= 20 else rival[:17] + "...", 1, 0, "L", 0)
        resultado = str(row["home_score"]) + " - " + str(row["away_score"])
        self.pdf.cell(55, 20, resultado, 1, 0, "C", 0)
        t2p = f"{row['t2p_conv']}/{row['t2p_int']} {self.locale_format(row['t2p_conv']/row['t2p_int']*100)}%"
        self.pdf.cell(70, 20, t2p, 1, 0, "C", 0)
        t3p = f"{row['t3p_conv']}/{row['t3p_int']} {self.locale_format(row['t3p_conv']/row['t3p_int']*100)}%"
        self.pdf.cell(70, 20, t3p, 1, 0, "C", 0)
        tl = f"{row['tl_conv']}/{row['tl_int']} {self.locale_format(row['tl_conv']/row['tl_int']*100)}%"
        self.pdf.cell(70, 20, tl, 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["reb_def"] + row["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["assists"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["steals"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(23, 20, str(row["efficience"]), 1, 0, "C", 0)

    def page_list_games(self):
        team = self.params["team_name"]
        list_games = self.data.list_games
        total_paginas = math.ceil(len(list_games)/20)
        pagina = 1
        fila = 1
        y = 70
        for index, row in self.data.list_games.iterrows():
            if fila == 1:
                self.create_page(f"{team}: Listado de partidos {pagina}/{total_paginas}")
                self.header_list_games(y)
                y = y + 20
                self.row_game(row, y)
            else:
                y = y + 20
                self.row_game(row, y)
            fila = fila + 1
            if fila > 20:
                #Nota a pie de página
                self.pdf.set_y(y + 25)
                self.set_advice()
                #Restablecemos indicadores
                fila = 1
                y = 70
                pagina = pagina + 1
        #Nota en la última página
        self.pdf.set_y(y + 25)
        self.set_advice()

    def page_standard_stats(self, params):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        away = "Rivales"
        home = params["team_name"]
        # print(f"object: {self.dpg.away_standard_stats}")
        home_ss = self.data.tss
        rivales_ss = self.data.oss
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
        home = params["team_name"]
        away = "Rivales"
        home_ss = self.data.tss
        home_as = self.data.tas
        opp_ss = self.data.oss
        opp_as = self.data.oas
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
        self.pdf.cell(200, 20, "Rivales", 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["rival_p_etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["p_reb_def"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["rival_p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(80, 20, self.locale_format(Decimal(opp_as["rival_ratio_ft"])), 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["p_reb_of"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["p_turnovers"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(70, 20, self.locale_format(Decimal(opp_as["ratio_ft"])), 1, 0, "C", 0)
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
         #Fila equipo rival
        self.pdf.set_y(270)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(200, 20, away, 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, self.locale_format(Decimal(opp_as["possessions"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(opp_as["possessions_x_minute"])), 1, 0, "C", 0)
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
        self.pdf.cell(45, 20, self.locale_format(opp_as["ortg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(opp_as["drtg"]), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(opp_as["nrtg"]), 1, 0, "C", 0)
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
        self.pdf.cell(42, 20, self.locale_format(Decimal(opp_as["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(42, 20, self.locale_format(Decimal(opp_as["ts"])) + "%", 1, 0, "C", 0)
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
        self.pdf.cell(45, 20, self.locale_format(Decimal(opp_as["assists_x_turnovers"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(opp_as["steals_x_turnovers"])), 1, 0, "C", 0)

    def shot_chart_team(self, tci):
        #get stats from shots from opponent team
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = AccumulatedTeamShots(self.params["destiny"], self.params["competition"])
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, ts.df, ts.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(ts.df, ss.df)
        #Save image
        name = f"accTeam-{self.params['destiny']}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def shot_chart_opp_team(self, tci):
        #get stats from shots from opponent team
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = AccumulatedOppShots(self.params["destiny"], self.params["competition"])
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, ts.df, ts.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(ts.df, ss.df)
        #Save image
        name = f"accOpp-{self.params['destiny']}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def page_team_graphics_1(self):
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = self.data.tss
        away_team = self.data.oss
        home_as = self.data.tas
        away_as = self.data.oas
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
        legends = [self.data.abrev, "Rivales"]
        labels = ["T2P%", "T3P%", "TL%", "BP%"]
        values = []
        values.append([home_2p, home_3p, home_1p, home_tov])
        values.append([away_2p, away_3p, away_1p, away_tov])
        file = str(self.params["destiny"]) + ".graphic5" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Distribución de posesiones", "Porcentaje")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [self.data.abrev, "Rivales"]
        labels = ["T2P", "T3P", "TL"]
        home_t1p = home_team["p_tl_puntos"]
        home_t2p = home_team["p_t2p_puntos"]
        home_t3p = home_team["p_t3p_puntos"]
        away_t1p = away_team["p_tl_puntos"]
        away_t2p = away_team["p_t2p_puntos"]
        away_t3p = away_team["p_t3p_puntos"]
        values = [[home_t2p, home_t3p, home_t1p], [away_t2p, away_t3p, away_t1p]]
        file = str(self.params["destiny"]) + ".graphic6" + IMAGES.EXTENSION
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
        home_team = self.data.tss
        away_team = self.data.oss
        home_as = self.data.tas
        away_as = self.data.oas
        self.pdf.set_y(75)
        legends = [self.data.abrev, "Rivales"]
        labels = ["Pace", "PPI", "PPP"]
        values = []
        values.append([home_as["possessions_x_minute"], home_team["ppa"], home_team["pointsbyposs"]])
        values.append([away_as["possessions_x_minute"], away_team["ppa"], away_team["pointsbyposs"]])
        file = str(self.params["destiny"]) + ".graphic7" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Eficiencia", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
        #Gráfico derecha - arriba
        self.pdf.set_xy(420, 75)
        legends = [self.data.abrev, "Rivales"]
        labels = ["RD/P", "RO/P", "TR/P"]
        values = [[home_team["reb_def_pp"], home_team["reb_of_pp"], home_team["total_rebs_pp"]], [away_team["reb_def_pp"], away_team["reb_of_pp"], away_team["total_rebs_pp"]]]
        file = str(self.params["destiny"]) + ".graphic8" + IMAGES.EXTENSION
        mb = MultiBarChatPlot(labels, values, legends, file, "Rebotes por partido", "")
        mb.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)

    def page_player_graphics(self):
        labels = [player["name"] for player in self.data.list_players]
        total_points = self.data.tss["total_puntos"]
        values = [round(Decimal(player["total_puntos"]/total_points*100), 2) for player in self.data.points_players]
        file = str(self.params["destiny"]) + ".player.graphic.2" + IMAGES.EXTENSION
        barchart = BarChartPlot(labels, values, file, "Distribución de puntos por jugadora", "Porcentaje")
        barchart.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 550)
        self.pdf.set_xy(PDFK.LANDSCAPE_A4_WIDTH/2 - width/2, 65)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
