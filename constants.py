class BCOLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class COMPETITIONS:
    LF1 = "FEB-LF1"
    LF2 = "FEB-LF2"
    EUROLEAGUE = "FIBA-Euroleague"
    EUROCUP = "FIBA-Eurocup"


class DDBB(object):
    DDBB_HOST = "localhost"
    DDBB_USER = "root"
    DDBB_PSWD = "123456"
    DDBB_NAME = "feb_estadisticas"
    #DDBB_NAME = "estadisticas2"
    DDBB_CHARSET = "latin1"
    DDBB_FIBA_HOST = "localhost"
    DDBB_FIBA_USER = "root"
    DDBB_FIBA_PSWD = "123456"
    #DDBB_FIBA_NAME = "fiba_stats"
    DDBB_FIBA_NAME = "fiba_stats_dev"
    DDBB_FIBA_CHARSET = "utf8"


class FORMAT(object):
    DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
    DATE_FORMAT_SHORT = "%d/%m/%Y"
    DATE_FORMAT_INVERSE = "%Y/%m/%d %H:%M:%S"
    DATE_FORMAT_DAY = "%Y/%m/%d"
    DATE_FORMAT_HOUR = "%H:%M"
    DATE_FORMAT_FILE = "%Y-%m-%d-%H-%M-%S"
    IMAGE_WIDTH = 800


class IMAGES:
    IMAGE_ROUTE = "output/images/"
    EXTENSION = ".png"
    FIBA_COLOUR_MAP = "files/images/fiba-campo.jpg"
    FEB_LEFT_COLOUR_MAP = "files/images/feb-left.png"
    FEB_RIGHT_COLOUR_MAP = "files/images/feb-right.png"
    TEST_COLOUR_MAP = "files/images/fiba-field.png"
    BASKET_COURT = "files/images/campo.png"
    FONTS_ROUTE = "files/fonts/"
    BACKGROUND_COLOR_R = 6
    BACKGROUND_COLOR_G = 47
    BACKGROUND_COLOR_B = 75

class LANGUAGE(object):
    SPANISH = "es"
    ENGLISH = "en"


class PDFK:
    PORTRAIT_A4_WIDTH = 595.28   #Size in points. 72 points = 1 inch
    PORTRAIT_A4_HEIGHT = 841.89  #Size in points. 72 points = 1 inch
    LANDSCAPE_A4_WIDTH = 841.89
    LANDSCAPE_A4_HEIGHT = 595.28
    REPORT_ROUTES = "output/reports/"

class RESULT(object):
    RESULT_OK = 0
    RESULT_TAG_NOT_FOUND = 1
    RESULT_SYSTEM_ERROR = 3


class URL(object):
    FILE_QUERYS = "./files/querys.sql"
    LOG = "./log/logfile.txt"
    ROUTE_TO_QUERYS = "./files/"
    ROUTE_TO_IMAGES = "./files/images/"
    ROUTE_TO_BASE = "./files/images/base/"
    ROUTE_TO_IMAGES_TWITTER = "./files/images/twitter/"
    ROUTE_TO_FOOT = "./files/images/pie.jpg"
    ROUTE_TO_LOGO = "./files/images/logo-basketmetrics.png"

class SEASONS:
    LF1_SEASON = 45
    LF2_SEASON = 46
    EUROLEAGUE_SEASON = 3
    EUROCUP_SEASON = 4
