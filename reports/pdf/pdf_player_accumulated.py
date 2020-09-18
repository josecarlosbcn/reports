from reports.pdf.pdf_file import PDFFile
from constants import PDFK, COMPETITIONS,IMAGES
from pathlib import Path
import os, locale
from datetime import datetime
from decimal import Decimal
from com.shotchart.shots.season_shots import SeasonShots
from com.shotchart.shots.player_shots import PlayerShots
from com.shotchart.images.shotchartimage import ShotChartImage


class PDFPlayerAccumulated(PDFFile):
    def __init__(self, params, data_accumulated):
        '''
            Los parámetros recibidos son:
            "id": None -> id of tbl003_player
            "id_player_team": 10213 --> id of tbl006_player_team
            "date": "15/05/2020",
            "id_season": 45,
            "competition": "FEB-LF1"
        '''
        print(f"Params PDFPlayerAccumulated: {params}")
        super().__init__(params)
        self.data = data_accumulated
        print("PDFPlayerAccumulated:: Creamos PDF")
        self.cover()
        print("PDFPlayerAccumulated:: Creando página comparativa de estadísticas estándar y avanzadas")
        self.player_pages(params)
        print("PDFShotChart:: Creando página de tiro de la jugadora")
        if params["competition"] == COMPETITIONS.LF1 or params["competition"] == COMPETITIONS.EUROLEAGUE \
            or params["competition"] == COMPETITIONS.EUROCUP:
            self.create_page(f"Carta de tiro: {self.data.name.title()}")
            print(f"\tGenerating shotchart of player: {self.data.name}")
            if len(self.data.pss) > 1:
                suma = 0
                for item in self.data.pss:
                    suma = suma + item["tc_int"]
                self.shot_chart_player(suma)
            else:
                self.shot_chart_player(self.data.pss[0]["tc_int"])
        #Glosario
        print("PDFPreGame:: Creando glosario")
        self.create_page("Glosario 1/2")
        self.page_glosario_1()
        self.create_page("Glosario 2/2")
        self.page_glosario_2()
        print("PDFAccumulated:: Vamos a guardar PDF")
        self.save_pdf(params)

    def player_pages(self, params):
        title = "Estadísticas estándard y avanzadas"
        if len(self.data.pss) > 1:    #Player has played in more than one team
            pss = self.data.pss
            pas = self.data.pas
            for i in range(len(pss)):
                title = f"Estadísticas estándard y avanzadas {i+1}/{len(pss)}: {self.data.name}"
                self.player_stats(title, pss[i], pas[i])
            #self.player_stats_2(pss, pas)
        else:   #Player has played in only one team
            pss = self.data.pss[0]
            pas = self.data.pas[0]
            title = f"Estadísticas estándard y avanzadas: {self.data.name}"
            self.player_stats(title, pss, pas)

    def player_stats(self, title, stats, adv):
        '''
            Build of the unique page of player statistics. Here we are showing standard and avanced stats
        :param stats: Player standard stats
        :param adv: Player advanced stats
        :return:
        '''
        self.create_page(title)
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
        #Nombre equipo
        self.pdf.set_y(65)
        self.pdf.set_font("Arial", "", 14)
        team = f"Equipo: {stats['name']}"
        self.pdf.text(30, 75, team)
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(90)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de tiro totales") + 5, 15, "Estadísticas de tiro totales", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(115)
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
        self.pdf.set_y(135)
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
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tc_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tl_conv"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["tl_int"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["tl_percentage"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, str(stats["total_puntos"]), 1, 0, "C", 0)
        #Tabla Estadísticas de distribución de tiros
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_xy(640, 90)
        self.pdf.cell(self.pdf.get_string_width("Distribución de puntos") + 5, 15, "Distribución de puntos", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_xy(640, 115)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, "PJ", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "2P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "3P%", 1, 0, "C", 1)
        self.pdf.cell(40, 20, "TL%", 1, 0, "C", 1)
        #Fila estadísticas
        self.pdf.set_font("Arial", "", 10)
        self.pdf.set_xy(640, 135)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t2p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_t3p_puntos"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(stats["p_tl_puntos"])) + "%", 1, 0, "C", 0)
        #Tabla Estadísticas de distribución de tiros por partido
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(175)
        self.pdf.cell(self.pdf.get_string_width("Distribución de tiros por partido") + 5, 15, "Distribución de tiros por partido", "B: 1", 1, "L")
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(200)
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
        self.pdf.set_y(225)
        self.pdf.set_fill_color(225, 225, 225)
        self.pdf.cell(40, 20, str(int(stats["games"])), 1, 0, "C", 0)
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
        self.pdf.set_y(265)
        self.pdf.cell(self.pdf.get_string_width("Estadísticas de rebote") + 5, 15, "Estadísticas de rebote", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(290)
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
        self.pdf.set_y(310)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(60, 20, str(stats["games"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["reb_def"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["reb_def_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["reb_of"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["reb_of_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, str(stats["total_rebs"]), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(stats["total_rebs_pp"])), 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_reb_def"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_reb_of"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(60, 20, self.locale_format(Decimal(adv["p_tot_reb"])) + "%", 1, 0, "C", 0)
        #Eficiencia
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(345)
        self.pdf.cell(self.pdf.get_string_width("Eficiencia") + 5, 15, "Eficiencia", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(370)
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
        self.pdf.set_y(390)
        self.pdf.set_font("Arial", "", 10)
        self.pdf.cell(45, 20, str(stats["games"]), 1, 0, "C", 0)
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
        self.pdf.set_y(425)
        self.pdf.cell(self.pdf.get_string_width("Otras estadísticas totales y por partido") + 5, 15, "Otras estadísticas totales y por partido", "B: 1", 1, "L")
        self.pdf.set_font("Arial", "B", 14)
        #Cabecera
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.set_y(450)
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
        self.pdf.set_y(470)
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
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["game_score"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["dre"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["p_assists"])) + "%", 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["assists_x_turnovers"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["assists_ratio"])), 1, 0, "C", 0)
        self.pdf.cell(40, 20, self.locale_format(Decimal(adv["p_steals"])) + "%", 1, 0, "C", 0)


    def player_stats_2(self, pss, pas):
        '''
            Build of the two pages version of player statistics
        :param pss:
        :param pas:
        :return:
        '''
        self.create_page("Estadísticas estándard y avanzadas 1/2")
        self.create_page("Estadísticas estándard y avanzadas 2/2")

    def set_title_cover(self):
        self.pdf.set_font('Arial', 'B', 32)
        #self.pdf.set_text_color(4, 52, 116)
        name_player = self.data.name
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(name_player)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 96, name_player)
        self.pdf.set_font('Arial', '', 26)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width(self.data.season)/2, PDFK.LANDSCAPE_A4_HEIGHT/2 - 60, self.data.season)

    def set_type_inform_cover(self):
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.text(PDFK.LANDSCAPE_A4_WIDTH/2 - self.pdf.get_string_width("Estadísticas acumuladas")/2, PDFK.LANDSCAPE_A4_HEIGHT/2, "Estadísticas acumuladas")

    def save_pdf(self, params):
        Path(PDFK.REPORT_ROUTES).mkdir(parents=True, exist_ok=True)
        directory = self.params["destiny"] if ("destiny" in self.params and self.params["destiny"] is not None) else "players"
        print(f"directory: {directory}")
        if directory == "players " and not os.path.exists(PDFK.REPORT_ROUTES + "players"):
            os.makedirs(PDFK.REPORT_ROUTES + "players")
        #print("Existe? {}".format(os.path.exists(str(params["destiny"]))))
        route_file = PDFK.REPORT_ROUTES + str(directory) + "/" + params["type"] + "-" + self.data.name_url + ".pdf"
        print(f"route_file: {route_file}")
        self.fileName = route_file
        self.pdf.output(route_file)
        print(f"PDF guardado: {route_file}")

    def shot_chart_player(self, tci):
        #get stats of shots from opponent team and players
        ss = SeasonShots(self.params["competition"], self.get_season(self.params["competition"]))
        ps = PlayerShots(self.params)
        self.set_advertencia(tci, ps.df, ps.errores)
        #get image and set stats over image
        image = ShotChartImage(IMAGES.BASKET_COURT)
        image.resize_from_width(500)
        image.set_data_over_image(ps.df, ss.df)
        id1 = self.params["id"] if id in self.params else self.params["id_player_team"]
        name = f"{id1}.shotchart.png"
        image.save_image(IMAGES.IMAGE_ROUTE + name)
        #Tabla Estadísticas de tiro
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_y(75)
        self.pdf.cell(self.pdf.get_string_width("Carta de tiro equipo") + 5, 15, "Carta de tiro equipo", "B: 1", 1, "L")
        self.pdf.image(IMAGES.IMAGE_ROUTE + name, 28, 65)
        image.remove_image(IMAGES.IMAGE_ROUTE + name)
