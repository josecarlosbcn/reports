from reports.pdf.pdf_file import PDFFile
from reports.pdf.pdf_pregame import PDFPreGame
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


class PDFPressPreGame(PDFFile):
    def __init__(self, params, data_pre_game):
        super().__init__(params)
        self.dpg = data_pre_game
        #Creamos página principal
        self.cover()
        print("PDFPressPreGame:: Creando página comparativa de estadísticas estándar")
        self.create_page("Comparativa de estadísticas estándar")
        self.page_standard_stats(params, self.dpg.home_standard_stats, self.dpg.away_standard_stats)
        print("PDFPressPreGame:: Creando página comparativa de estadísticas avanzadas")
        self.create_page("Comparativa de estadísticas avanzadas")
        self.page_advanced_stats(params, data_pre_game)
        #Carta de tiro de equipo
        print("PDFPressPreGame:: Creando carta de tiro de los equipos")
        home = params["home_team"]
        away = params["away_team"]
        if params["competition"] != COMPETITIONS.LF2:
            self.create_page(f"Carta de tiro: {home}")
            #Hay que filtrar por equipo por id_game
            self.shot_chart_team(params["home"], self.dpg.home_standard_stats[0]['tc_int'])
            self.create_page(f"Carta de tiro: {away}")
            self.shot_chart_team(params["away"], self.dpg.away_standard_stats[0]['tc_int'])
        print("PDFPressPreGame:: Creando página con gráficas comparativas entre equipos")
        self.create_page("Gráficas comparativas entre equipos 1/2")
        self.page_team_graphics_1(self.dpg.home_standard_stats, self.dpg.away_standard_stats)
        self.create_page("Gráficas comparativas entre equipos 2/2")
        self.page_team_graphics_2(self.dpg.home_standard_stats, self.dpg.away_standard_stats, self.dpg.home_advanced_stats, self.dpg.away_advanced_stats)
        print("PDFPressPreGame:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        self.save_pdf(params)

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.cell(PDFK.A4_WIDTH, PDFK.A4_HEIGHT/2, team_name, border = 0, align = "C")
        #self.pdf.set_text_color(4, 52, 116)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["home_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, self.params["home_team"])
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("vs")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, "vs")
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.params["away_team"])/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 24, self.params["away_team"])
        self.pdf.set_font('Arial', '', 18)
        date = "Fecha partido: " + self.dpg.params['date_game'].strftime('%d/%m/%Y %H:%M')
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(date)/2, PDFK.LANDSCAPE_A4_HEIGHT/2, date)

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Informe pre-partido")/2, PDFK.LANDSCAPE_A4_HEIGHT/2 + 50, "Informe pre-partido")

    def shot_chart_team(self, id_team, tci):
        #get stats from shots from opponent team
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ts = TeamShots(id_team, self.params["competition"])
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

    def save_pdf(self, params):
        Path(PDFK.REPORT_ROUTES).mkdir(parents=True, exist_ok=True)
        #print("Existe? {}".format(os.path.exists(str(params["destiny"]))))
        if not os.path.exists(PDFK.REPORT_ROUTES + "prensa"):
            os.makedirs(PDFK.REPORT_ROUTES + "prensa")
        route_file = PDFK.REPORT_ROUTES + "prensa/preGame-" + params["home_url"] + ".vs." + params["away_url"] + ".pdf"
        self.fileName = route_file
        self.pdf.output(route_file)
        print(f"PDF guardado: {route_file}")
