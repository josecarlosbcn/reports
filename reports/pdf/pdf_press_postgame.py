from reports.pdf.pdf_file import PDFFile
from constants import PDFK, COMPETITIONS,IMAGES
from com.shotchart.shots.team_shots import TeamShots
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.images.shotchartimage import ShotChartImage
import locale
from decimal import Decimal
from com.graphics.doublebar_chart_plot import MultiBarChatPlot
import os
from com.graphics.bar_chart_plot import BarChartPlot
from pathlib import Path
import datetime


class PDFPressPostGame(PDFFile):
    def __init__(self, params, data_post_game):
        super().__init__(params)
        self.dpg = data_post_game
        #Creamos página principal
        self.cover()
        #Creamos página comparativa de estadísticas
        print("PDFPressPostGame:: Creando página comparativa de estadísticas estándar")
        self.create_page("Comparativa de estadísticas estándar")
        self.page_standard_stats(params, self.dpg.home_standard_stats, self.dpg.away_standard_stats)
        print("PDFPressPostGame:: Creando página comparativa de estadísticas avanzadas")
        self.create_page("Comparativa de estadísticas avanzadas")
        self.page_advanced_stats(params, data_post_game)
        #Carta de tiro de equipo
        print("PDFPressPostGame:: Creando carta de tiro de los equipos")
        home = params["home_team"]
        away = params["away_team"]
        if params["competition"] != COMPETITIONS.LF2:
            self.create_page(f"Carta de tiro: {home}")
            #Hay que filtrar por equipo por id_game
            self.shot_chart_team_game(self.dpg.id_game, self.params["home"], self.dpg.home_standard_stats[0]['tc_int'])
            self.create_page(f"Carta de tiro: {away}")
            self.shot_chart_team_game(self.dpg.id_game, self.params["away"], self.dpg.away_standard_stats[0]['tc_int'])
        #Comparativas
        print("PDFPressPostGame:: Creando página con gráficas comparativas entre equipos")
        self.create_page("Gráficas comparativas entre equipos 1/2")
        self.page_team_graphics_1(self.dpg.home_standard_stats, self.dpg.away_standard_stats)
        self.create_page("Gráficas comparativas entre equipos 2/2")
        self.page_team_graphics_2(self.dpg.home_standard_stats, self.dpg.away_standard_stats, self.dpg.home_advanced_stats, self.dpg.away_advanced_stats)
        print("PDFPressPostGame:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        self.save_pdf(params)

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.set_text_color(4, 52, 116)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["home_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, self.params["home_team"])
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("vs")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, "vs")
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["away_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 24, self.params["away_team"])
        self.pdf.set_font('Arial', '', 18)
        date = "Fecha partido: " + self.dpg.params['date_game'].strftime('%d/%m/%Y %H:%M')
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(date)/2, PDFK.LANDSCAPE_A4_HEIGHT/2, date)

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Informe post-partido")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 + 50, "Informe post-partido")

    def page_standard_stats(self, params, hss, ass):
        '''

            :param params: Values given in the menu
            :param hss: Home standard stats
            :param ass: Away standard stats
        :return:
        '''
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #print (str( locale.getlocale() ))
        away = params["away_team"]
        home = params["home_team"]
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

    def page_team_graphics_2(self, hss, ass, has, aas):
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

    def save_pdf(self, params):
        Path(PDFK.REPORT_ROUTES).mkdir(parents=True, exist_ok=True)
        #print("Existe? {}".format(os.path.exists(str(params["destiny"]))))
        if not os.path.exists(PDFK.REPORT_ROUTES + "prensa"):
            os.makedirs(PDFK.REPORT_ROUTES + "prensa")
        route_file = PDFK.REPORT_ROUTES + "prensa/postGame-" + params["home_url"] + ".vs." + params["away_url"] + ".pdf"
        self.fileName = route_file
        self.pdf.output(route_file)
        print(f"PDF guardado: {route_file}")
