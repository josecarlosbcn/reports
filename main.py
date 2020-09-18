import os, sys
from constants import BCOLORS, COMPETITIONS
from reports.pregame import PreGame
from reports.postgame import PostGame
from reports.monthly import Monthly
from reports.team_accumulated import TeamAccumulated
from reports.player_accumulated import PlayerAccumulated
from reports.press import PressReport
import datetime


def clean_screen():
    '''Clean the screen of the console'''
    clear = lambda:os.system('clear')
    clear()


def exit():
    print(BCOLORS.OKBLUE + "See you later, alligator!!!" + BCOLORS.ENDC)


def doReportPreGame(params):
    r = PreGame(params)


def doReportPostGame(params):
    r = PostGame(params)


def doReportMonthly(params):
    r = Monthly(params)


def doReportTeamAccumulated(params):
    r1 = TeamAccumulated(params)
    ##Falta informes para jugadoras

def doReportPlayerAccumulated(params):
    r = PlayerAccumulated(params)

def doReportPress(params):
    r = PressReport(params)

def menuPreGame():
    destiny = menuDestiny()
    league = menuCompetition()
    teams = menuTeams()
    fecha = menuDateGame()
    return {
        "report": 1,
        "destiny": destiny,
        "date": fecha,
        "competition": league,
        "home": teams["home"],
        "away": teams["away"],
    }

def menuPostGame():
        destiny = menuDestiny()
        league = menuCompetition()
        teams = menuTeams()
        fecha = menuDateGame()
        return {
            "report": 2,
            "destiny": destiny,
            "date": fecha,
            "competition": league,
            "home": teams["home"],
            "away": teams["away"],
        }


def menuMonthly():
        destiny = menuDestiny()
        league = menuCompetition()
        team = menuTeam()
        date = menuDate()
        return {
            "report": 3,
            "destiny": destiny,
            "competition": league,
            "home": team["home"],
            "away": None,
            "month": date["month"],
            "year": date["year"]
        }

def menuTeamAccumulated():
        destiny = menuDestiny()
        league = menuCompetition()
        season = menuSeason()
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        return {
            "report": 4,
            "destiny": destiny,
            "competition": league,
            "id_season": season,
            "date": date
        }

def menuPlayerAccumulated():
        player = menuPlayer()
        season = menuSeason()
        competition = menuCompetition()
        today = datetime.date.today()
        date = today.strftime("%d/%m/%Y")
        return {
            "report": 5,
            "id": player,
            "id_player_team": None,
            "date": date,
            "id_season": season,
            "competition": competition
        }


def menuTypeReport():
    clean_screen()
    print("SELECCIONA TIPO DE INFORME")
    print("=============================")
    print("\t6. Informe pre-partido de un equipo")
    print("\t7. Informe pre-partido de una jornada")
    print("\t8. Informe post-partido de un partido")
    print("\t9. Informe post-partido de una jornada")
    print("\t0. Salir")
    option = None
    while option not in [6, 7, 8, 9, 0]:
        option = int(input("Opción: "))
    return option if option != 0 else sys.exit(0)

def menuSelectTeam():
    clean_screen()
    option = None
    while option is None:
        option = int(input("Introduce id del equipo: "))
    return option

def menuSelectGame():
    clean_screen()
    option = None
    while option is None:
        option = int(input("Introduce id del partido: "))
    return option

def menuSelectGameDay():
    clean_screen()
    option = None
    while option is None:
        option = int(input("Introduce id de la jornada: "))
    return option

def menuPress():
    type_report = menuTypeReport()
    id_team = None
    id_game = None
    id_jornada = None
    if type_report == 6:
        id_team = menuSelectTeam()
    if type_report == 8:
        id_game = menuSelectGame()
    if type_report == 9:
        id_jornada = menuSelectGameDay()
    id_competition = menuCompetition()
    today = datetime.date.today()
    date = today.strftime("%d/%m/%Y")
    return {
        "report": type_report,
        "id_jornada": id_jornada,
        "id_game": id_game,
        "team": id_team,
        "competition": id_competition,
        "date": date
    }

def menu():
    return {
         # "report": 2,
         # "destiny": 770,
         # "date": "15/05/2020 15:38",
         # "competition": "FEB-LF1",
         # "home": 770,
         # "away": 769,
        # "report": 3,
        # "destiny": 770,
        # "competition": "FEB-LF1",
        # "home": 770,
        # "month": 3,
        # "year": 2020
        # "report": 4,
        # "destiny": 770,
        # "competition": "FEB-LF1",
        # "home": 770,
        # "away": None,
        # "id_season": 45,
        # "date": "15/05/2020"
        # "report": 5,
        # "id": 2063,
        # "id_player_team": None,
        # "date": "15/05/2020",
        # "id_season": 45,
        # "competition": "FEB-LF1"
        # "report": 6,
        # "team": 822,
        # "competition" : "FEB-LF1",
        # "date": "15/09/2020"
        'report': 8,
        'id_jornada': None,
        'id_game': 10946,
        'team': None,
        'competition': 'FEB-LF1',
        'date': '15/09/2020',
    }
    report = mainMenu()
    values = switchMenu(report)
    return values

def mainMenu():
    clean_screen()
    print("SELECCIONA EL TIPO DE INFORME")
    print("=============================")
    print("\t1. Informe Pre-Partido")
    print("\t2. Informe Post-Partido")
    print("\t3. Informe Mensual")
    print("\t4. Informe Acumulado de Equipo")
    print("\t5. Informe jugadora")
    print("\t6. Informe prensa")
    print("\t0. Salir\n")
    report = None
    while report not in [1, 2, 3, 4, 5, 6, 0]:
        report = int(input("Opción: "))
    return report

def menuCompetition():
    clean_screen()
    print("SELECCIONA UNA COMPETICION")
    print("=============================")
    print("\t1. Liga Femenina 1")
    print("\t2. Liga Femenina 2")
    print("\t3. Euroleague Women")
    print("\t4. Eurocup Women")
    print("\t0. Salir\n")
    option = None
    while option not in [1, 2, 3, 4, 0]:
        option = int(input("Opción: "))
    option = switchCompetition(option)
    return option


def menuDate():
    clean_screen()
    month = None
    while not isinstance(month, int):
        month = int(input("Introduce el mes del informe: "))
    year = None
    while not isinstance(year, int):
        year = int(input("Introduce el año del informe (yyyy): "))
    return {
        "month": month,
        "year": year
    }

def menuDateGame():
    clean_screen()
    return input("Introduce la fecha del partido (dd/mm/yyyy hh:mm): ")


def menuDestiny():
    clean_screen()
    id_team = None
    while not isinstance(id_team, int):
        id_team = int(input("Introduce el identificador del equipo destino del informe: "))
    return id_team


def menuGame():
    clean_screen()
    id_game = None
    while not isinstance(id_game, int):
        id_game = int(input("Introduce el identificador de partido: "))
    return id_game

def menuPlayer():
    clean_screen()
    id = None
    while not isinstance(id, int):
        id = int(input("Introduce el identificador de jugadora (tbl003_player): "))
    return id

def menuSeason():
    clean_screen()
    id = None
    while not isinstance(id, int):
        id = int(input("Introduce el identificador de temporada: "))
    return id

def menuTeam():
    clean_screen()
    team = None
    while not isinstance(team, int):
        team = int(input("Introduce identificador del equipo: "))
    return {
        "home": team
    }


def menuTeams():
    clean_screen()
    home = None
    while not isinstance(home, int):
        home = int(input("Introduce identificador del equipo local: "))
    away = None
    while not isinstance(away, int):
        away = int(input("Introduce idenfiticador del equipo visitante: "))
    return {
        "home": home,
        "away": away
    }


def main():
    values = menu()
    switch(values["report"], values)


def switch(case, params):
    sw = {
        1: doReportPreGame,
        2: doReportPostGame,
        3: doReportMonthly,
        4: doReportTeamAccumulated,
        5: doReportPlayerAccumulated,
        6: doReportPress,
        7: doReportPress,
        8: doReportPress,
        9: doReportPress
    }
    return sw[case](params)

def switchMenu(case):
    sw = {
        0: exit,
        1: menuPreGame,
        2: menuPostGame,
        3: menuMonthly,
        4: menuTeamAccumulated,
        5: menuPlayerAccumulated,
        6: menuPress
    }
    return sw[case]()


def switchCompetition(case):
    sw = {
        1: COMPETITIONS.LF1,
        2: COMPETITIONS.LF2,
        3: COMPETITIONS.EUROLEAGUE,
        4: COMPETITIONS.EUROLEAGUE
    }
    return sw[case]

main()
