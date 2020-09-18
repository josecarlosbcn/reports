from reports.pdf.pdf_file import PDFFile
from constants import PDFK
from decimal import Decimal
import locale
from constants import COMPETITIONS, IMAGES
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.images.shotchartimage import ShotChartImage
from com.graphics.doublebar_chart_plot import MultiBarChatPlot
import os
from com.graphics.bar_chart_plot import BarChartPlot


class PDFPostGame(PDFFile):
    def __init__(self, params, data_post_game):
        super().__init__(params)
        self.dpg = data_post_game
        #Creamos página principal
        self.cover()
        #Creamos página comparativa de estadísticas
        print("PDFPostGame:: Creando página comparativa de estadísticas estándar")
        self.create_page("Comparativa de estadísticas estándar")
        self.page_standard_stats(params)
        print("PDFPostGame:: Creando página comparativa de estadísticas avanzadas")
        self.create_page("Comparativa de estadísticas avanzadas")
        self.page_advanced_stats(params, data_post_game)
        #Carta de tiro de equipo
        print("PDFPostGame:: Creando carta de tiro de los equipos")
        home = params["home_team"]
        away = params["away_team"]
        if params["competition"] != COMPETITIONS.LF2:
            self.create_page(f"Carta de tiro: {home}")
            #Hay que filtrar por equipo por id_game
            self.shot_chart_team_game(self.dpg.id_game, self.params["home"], self.dpg.home_standard_stats[0]['tc_int'])
            self.create_page(f"Carta de tiro: {away}")
            self.shot_chart_team_game(self.dpg.id_game, self.params["away"], self.dpg.away_standard_stats[0]['tc_int'])
        #Comparativas
        print("PDFPostGame:: Creando página con gráficas comparativas entre equipos")
        self.create_page("Gráficas comparativas entre equipos 1/2")
        self.page_team_graphics_1()
        self.create_page("Gráficas comparativas entre equipos 2/2")
        self.page_team_graphics_2()
        #Estadísticas de jugadoras y cartas de tiro de jugadoras
        print("PDFPostGame:: Creando páginas de estadísticas y carta de tiro de jugadoras")
        self.players_page(params)
        #Gráficas de jugadoras
        self.create_page("Gráficas comparativas entre jugadoras")
        self.page_player_graphics()
        #Glosario
        print("PDFPostGame:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        print("PDFPostGame:: Vamos a guardar PDF")
        self.save_pdf(params)

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.set_text_color(4, 52, 116)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["home_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, self.params["home_team"])
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("vs")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, "vs")
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["away_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 24, self.params["away_team"])

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Informe post-partido")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 + 50, "Informe post-partido")

    def page_standard_stats(self, params):
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        away = params["away_team"]
        home = params["home_team"]
        away_ss = self.dpg.away_standard_stats[0]
        home_ss = self.dpg.home_standard_stats[0]
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
        # #Estadísticas de rebotes
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(180)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de rebote totales") + 5, 15, "Estadísticas de rebote totales", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(205)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(225)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(home_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(home_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(home_ss["total_rebs"]), 1, 0, "C", 0)
        #Fila equipo visitante
        self.pdf.set_y(245)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(away_ss["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(away_ss["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(away_ss["total_rebs"]), 1, 0, "C", 0)
        # #Otras estadísticas
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(285)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales") + 5, 15, "Otras estadísticas totales", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(310)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(200, 20, "EQUIPOS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BR", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FC", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "FR", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "VAL.", 1, 0, "C", 1)
        #Fila equipo local
        self.pdf.set_y(330)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, home.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(home_ss["assists"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["steals"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(home_ss["efficience"]), 1, 0, "C", 0)
        #Fila equipo
        self.pdf.set_y(350)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(200, 20, away.title(), 1, 0, "L", 1)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(40, 20, str(away_ss["assists"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["steals"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(away_ss["efficience"]), 1, 0, "C", 0)

    def shot_chart_team_game(self, id_game, id_team, tci):
        '''
            Short chart for an only game.
        :param id_game:
        :param id_team:
        :param tci:
        :return:
        '''
        #get stats from shots from opponent team
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(id_team, self.params["competition"])
        data = ts.df.query(f"id_game == {id_game}")
        errores = data.query(f"id_game == {id_game} and position.isnull()")
        #print(f"Total lanzamientos equipo: {len(ts.df)}")
        #print(f"Total lanzmientos temporada: {len(ss.df)}")
        self.set_advertencia(tci, data, len(errores))
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        #Set data over image
        image.set_data_over_image(data, ss.df)
        #Save image
        name = f"{id_team}.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)

    def page_team_graphics_1(self):
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = self.dpg.home_standard_stats[0]
        away_team = self.dpg.away_standard_stats[0]
        home_as = self.dpg.home_advanced_stats[0]
        away_as = self.dpg.away_advanced_stats[0]
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
        legends = [self.dpg.home_standard_stats[0]["abrev"], self.dpg.away_standard_stats[0]["abrev"]]
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
        legends = [self.dpg.home_standard_stats[0]["abrev"], self.dpg.away_standard_stats[0]["abrev"]]
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

    def page_team_graphics_2(self):
        #print(stats)
        #Gráfico izquierdo - arriba
        #Calculo de % de lanzamientos
        home_team = self.dpg.home_standard_stats[0]
        away_team = self.dpg.away_standard_stats[0]
        home_as = self.dpg.home_advanced_stats[0]
        away_as = self.dpg.away_advanced_stats[0]
        self.pdf.set_y(75)
        legends = [self.dpg.home_standard_stats[0]["abrev"], self.dpg.away_standard_stats[0]["abrev"]]
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
        # self.pdf.set_xy(420, 75)
        # legends = [self.dpg.home_standard_stats[0]["abrev"], self.dpg.away_standard_stats[0]["abrev"]]
        # labels = ["RD/P", "RO/P", "TR/P"]
        # values = [[home_team["reb_def_pp"], home_team["reb_of_pp"], home_team["total_rebs_pp"]], [away_team["reb_def_pp"], away_team["reb_of_pp"], away_team["total_rebs_pp"]]]
        # file = str(self.params["home"]) + "." + str(self.params["away"]) + ".graphic4" + IMAGES.EXTENSION
        # mb = MultiBarChatPlot(labels, values, legends, file, "Rebotes por partido", "")
        # mb.save_file()
        # #Resize de la imagen a un ancho determinado
        # (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 400)
        # self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        # os.remove(IMAGES.IMAGE_ROUTE + file)

    def players_page(self, params):
        pss = self.dpg.home_pt_ss if params["destiny"] == params["home"] else self.dpg.away_pt_ss
        pas = self.dpg.home_pt_as if params["destiny"] == params["home"] else self.dpg.away_pt_as
        id_team = params["away"] if params["destiny"] == params["home"] else params["home"]
        if len(pss) != len(pas):
            raise Exception("PDFPostGame::players_page: El número de jugadoras en las estadísticas estándard no coincide con las avanzadas")
        for i in range(len(pss)):
            #print(f"Estadisticas estándar de {pss[i]['name']}, y estadisticas avanzadas de {pas[i]['name']}")
            self.create_page(f"Estadísticas estándar y avanzadas: {pss[i]['name'].title()}")
            self.players_page_stats(pss[i], pas[i])
            if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.EUROLEAGUE \
                or params["competition"] == COMPETITIONS.EUROCUP:
                self.create_page(f"Carta de tiro: {pss[i]['name'].title()}")
                print(f"\tGenerating shotchart of player: {pss[i]['name']}")
                self.shot_chart_player_game(self.dpg.id_game, pss[i]["id_player_team"], pss[i]["tc_int"])

    def players_page_stats(self, stats, adv):
        #print(stats)
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro totales") + 5, 15, "Estadísticas de tiro totales", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(100)
        self.pdf.set_fill_color(225, 225, 225)
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
        self.pdf.set_xy(600, 75)
        self.pdf.cell(self.pdf.get_string_width("Distribución de puntos") + 5, 15, "Distribución de puntos", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_xy(600, 100)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, "2P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "3P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_font("Arial", "", 10)
        self.pdf.set_xy(600, 120)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t2p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t3p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_tl_puntos"])) + "%", 1, 0, "C", 0)
        # #Tabla Estadísticas de distribución de tiros por partido
        # self.pdf.set_font("Arial", "B", 14)
        # self.pdf.set_y(155)
        # self.pdf.cell(self.pdf.get_string_width("Distribución de tiros por partido") + 5, 15, "Distribución de tiros por partido", "B: 1", 1, "L")
        # #Cabecera
        # self.pdf.set_font("Arial", "B", 10)
        # self.pdf.set_y(180)
        # self.pdf.set_fill_color(225, 225, 225)
        # self.pdf.cell(40, 20, "T2PC", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "T2PI", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "T2P%", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "T3PC", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "T3PI", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "T3P%", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TCC", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TCI", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TC%", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TLC", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TLI", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        # self.pdf.cell(40, 20, "PTOS", 1, 0, "C", 1)
        # #Fila estadísticas
        # self.pdf.set_font("Arial", "", 10)
        # self.pdf.set_y(200)
        # self.pdf.set_fill_color(225, 225, 225)
        # self.pdf.cell(40, 20, self.locale_format(stats["t2p_conv_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["t2p_int_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t2p_percentage"])) + "%", 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["t3p_conv_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["t3p_int_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(Decimal(stats["t3p_percentage"])) + "%", 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["tc_conv_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["tc_int_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tc_percentage"])), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["tl_conv_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["tl_int_pp"]), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tl_percentage"])), 1, 0, "C", 0)
        # self.pdf.cell(40, 20, self.locale_format(stats["total_puntos_pp"]), 1, 0, "C", 0)
        #Estadísticas de rebotespor partido
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(155)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de rebote") + 5, 15, "Estadísticas de rebote", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(180)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(60, 20, "RD", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RD%", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "RO%", 1, 0, "C", 1)
        self.pdf.cell(60, 20, "TR%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(200)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(stats["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_reb_def"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_reb_of"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_tot_reb"])) + "%", 1, 0, "C", 0)
        #Eficiencia
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(240)
        self.pdf.cell(self.pdf.get_string_width("Eficiencia") + 5, 15, "Eficiencia", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(265)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(45, 20, "PPP", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "PPI", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "USG%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "eTC%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "TS%", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "ORTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "DRTG", 1, 0, "C", 1)
        self.pdf.cell(45, 20, "NRTG", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(285)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, self.locale_format(Decimal(stats["pointsbyposs"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(stats["ppa"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["usg"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["etc"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["ts"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["ortg"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["drtg"])), 1, 0, "C", 0)
        self.pdf.cell(45, 20, self.locale_format(Decimal(adv["nrtg"])), 1, 0, "C", 0)
        #Otras estadísticas
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(320)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales y por partido") + 5, 15, "Otras estadísticas totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(345)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(35, 20, "AS", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BR", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "BP", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "TP", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FC", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "FR", 1, 0, "C", 1)
        self.pdf.cell(35, 20, "VAL.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "GS", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "DRE", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS/BP", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "AS.Rat.", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "BR%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_y(365)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(35, 20, str(stats["assists"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["steals"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["turnovers"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["block_shots"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["fouls_cm"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["fouls_rv"]), 1, 0, "C", 0)
        self.pdf.cell(35, 20, str(stats["efficience"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["game_score"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["dre"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["p_assists"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["assists_x_turnovers"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["assists_ratio"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["p_steals"])) + "%", 1, 0, "C", 0)

    def shot_chart_player_game(self, id_game, id_player_team, tci):
        #get stats of shots from opponent team and players
        id_team = self.params["home"] if self.params["destiny"] == self.params["home"] else self.params["away"]
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(id_team, self.params["competition"])
        ps = ts.df.query(f"id_game == {id_game} and id_player_team == {id_player_team}")
        #ps = PlayerShots(ts.id_team_club, ts.competition)
        errores = ps.query("position.isnull()")
        self.set_advertencia(tci, ps, len(errores))
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        image.set_data_over_image(ps, ss.df)
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
        players = self.dpg.home_pt_ss if self.params["destiny"] == self.params["home"] else self.dpg.away_pt_ss
        total_points = self.dpg.home_standard_stats[0]["total_puntos"] if self.params["destiny"] == self.params["home"] else self.dpg.away_standard_stats[0]["total_puntos"]
        labels = [player["name"] for player in players]
        values = [round(Decimal(player["total_puntos"]/total_points*100), 2) for player in players]
        file = str(self.params["home"]) + "." + str(self.params["away"]) + ".player.graphic.1" + IMAGES.EXTENSION
        barchart = BarChartPlot(labels, values, file, "Distribución de puntos por jugadora", "Porcentaje")
        barchart.save_file()
        #Resize de la imagen a un ancho determinado
        (width, height) = self.resize_image(IMAGES.IMAGE_ROUTE + file, 550)
        self.pdf.set_xy(PDFK.LANDSCAPE_A4_WIDTH/2 - width/2, 65)
        self.pdf.image(IMAGES.IMAGE_ROUTE + file, w=width, h=height)
        os.remove(IMAGES.IMAGE_ROUTE + file)
