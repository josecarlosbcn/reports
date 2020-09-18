from decimal import Decimal
from constants import BCOLORS


class TeamAS(object):
    def __init__(self, home_ss, away_ss):
        self.home_ss = home_ss
        self.away_ss = away_ss
        # for k, v in self.home_ss.items():
        #     print("key: {} - value: {}".format(k, v))
        self.etc = 0                #Effective Field Goal Percentage
        self.pto = 0                #Percentage Turnovers
        self.prd = 0                #Percentage Defensive Rebounds
        self.pro = 0                #Percentage Offensive Rebounds
        self.ratio_ft = 0           #Ratio Free Throws
        self.possessions = 0        #Total number of possessions
        self.poss_time = 0          #Number of possessions by minute
        self.rat = 0                #Ratio Assists / Turnovers
        self.rst = 0                #Ration Steals / Turnovers
        self.ts = 0                 #True Shoot %
        self.ortg = 0               #Offensive Rating
        self.drtg = 0               #Defensive Rating
        self.nrtg = 0               #Net Rating
        self.minutes = self.home_ss["minutes"]          #Minutos jugados
        self.make_calculus()

    def make_calculus(self):
        self.set_etc()
        self.set_percentage_reb_def()
        self.set_percentage_reb_of()
        self.set_rival_percentage_turnovers()
        self.set_percentage_turnovers()
        self.set_ratio_ft()
        self.set_rival_ratio_ft()
        self.set_rival_etc()
        #self.possessions = self.set_possessions(self.get_home_ss(), self.get_away_ss())
        self.set_possessions()
        self.set_possession_time()
        self.set_ratio_assists_turnovers()
        self.set_ratio_steals_turnovers()
        self.set_ts()
        self.set_ortg()
        self.set_drtg()
        self.set_nrtg()

    """Setters & Getters"""
    def get_home_ss(self):
        return self.home_ss

    def get_away_ss(self):
        return self.away_ss

    def get_minutes(self):
        return self.minutes

    def set_etc(self):
        """Method with which we calculate Effective Field Goal Percentage"""
        tc = self.get_home_ss()["t2p_conv"] + self.get_home_ss()["t3p_conv"]
        tci = self.get_home_ss()["t2p_int"] + self.get_home_ss()["t3p_int"]
        try:
            self.etc = round(((tc + Decimal('0.5') * self.get_home_ss()["t3p_conv"])/tci) * 100, 2)
        except:
            print(BCOLORS.FAIL + "Error: decimal.InvalidOperation" + BCOLORS.ENDC)
            self.etc = 0

    def get_etc(self):
        return self.etc

    def set_percentage_reb_def(self):
        """Method with which we calculate Percentage of Defensive Rebounds"""
        hss = self.get_home_ss()
        opp = self.get_away_ss()
        try:
            self.prd = round((int(hss["reb_def"])/(int(hss["reb_def"]) + int(opp["reb_of"])))*100, 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
            self.prd = 0

    def get_percentage_reb_def(self):
        return self.prd

    def set_percentage_reb_of(self):
        """Method with which we calculate Percentage of Offensive Rebounds"""
        hss = self.get_home_ss()
        opp = self.get_away_ss()
        try:
            self.pro = round((int(hss["reb_of"])/(int(hss["reb_of"]) + int(opp["reb_def"])))*100, 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
            self.pro = 0

    def get_percentage_reb_of(self):
        return self.pro

    def set_rival_percentage_turnovers(self):
        """Method with which we calculate Percentage Turnovers"""
        opp = self.get_away_ss()
        tci = int(opp["t2p_int"]) + int(opp["t3p_int"])
        self.rival_pto = round((int(opp["turnovers"])/(tci + (0.44*int(opp["tl_int"])) + int(opp["turnovers"])))*100, 2)

    def get_rival_percentage_turnovers(self):
        return self.rival_pto

    def set_percentage_turnovers(self):
        """Method with which we calculate Percentage Turnovers"""
        hss = self.get_home_ss()
        tci = int(hss["t2p_int"]) + int(hss["t3p_int"])
        self.pto = round((int(hss["turnovers"])/(tci + (0.44*int(hss["tl_int"])) + int(hss["turnovers"])))*100, 2)

    def get_percentage_turnovers(self):
        return self.pto

    def set_ratio_ft(self):
        """Method with which we calculate Ratio of Free Throws compared with the total of field goals
        attempted"""
        hss = self.get_home_ss()
        tci = int(hss["t2p_int"]) + int(hss["t3p_int"])
        try:
            self.ratio_ft = round(int(hss["tl_conv"])/tci, 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
            self.ratio_ft = 0

    def get_ratio_ft(self):
        return self.ratio_ft

    def set_rival_ratio_ft(self):
        """Method with which we calculate Ratio of Free Throws compared with the total of field goals
        attempted for the rival team"""
        opp = self.get_away_ss()
        tci = int(opp["t2p_int"]) + int(opp["t3p_int"])
        try:
            self.rival_ratio_ft = round(int(opp["tl_conv"])/tci, 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
            self.rival_ratio_ft = 0

    def get_rival_ratio_ft(self):
        return self.rival_ratio_ft

    def set_rival_etc(self):
        """Method with which we calculate Effective Field Goal Percentage for the rival team"""
        tc = self.get_away_ss()["t2p_conv"] + self.get_away_ss()["t3p_conv"]
        tci = self.get_away_ss()["t2p_int"] + self.get_away_ss()["t3p_int"]

        try:
            self.rival_etc = round(((float(tc) + float(0.5)*float(self.get_away_ss()["t3p_conv"]))/float(tci))*100, 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
            self.rival_etc = 0

    def get_rival_etc(self):
        return self.rival_etc

    def set_possessions(self):
        """Method which returns the total of possesions of a team
        hss: home_standard_stats
        opp: away_standard_stats"""
        hss = self.home_ss
        opp = self.away_ss
        teamFGA = int(hss["t2p_int"]) + int(hss["t3p_int"])
        teamFG = int(hss["t2p_conv"]) + int(hss["t3p_conv"])
        oppFGA = int(opp["t2p_int"]) + int(opp["t3p_int"])
        oppFG = int(opp["t2p_conv"]) + int(opp["t3p_conv"])

        try:
            x = int(hss["reb_of"]) + int(opp["reb_def"])
            y = int(hss["reb_of"])/x
            z = teamFGA - teamFG
            a = 1.07 * y * z
            b = 1.07 * (int(opp["reb_of"])/(int(opp["reb_of"]) + int(hss["reb_def"]))) * (oppFGA - oppFG)

            self.possessions = round(0.5 * ((teamFGA + (0.4 * int(hss["tl_int"])) - a + int(hss["turnovers"])) +
                                            (oppFGA + (0.4 * int(opp["tl_int"])) - b + int(opp["turnovers"]))), 2)
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error(set_possessions): División por cero" + BCOLORS.ENDC)
            self.possessions = -9

    def get_possessions(self):
        return self.possessions

    def set_possession_time(self):
        """Method which returns the number of possessions by minute"""
        self.poss_time = round(Decimal(self.get_possessions())/(Decimal(self.get_minutes())/5), 2)

    def get_possession_time(self):
        return self.poss_time

    def set_ratio_assists_turnovers(self):
        """Method which returns ratio assists / turnovers"""
        if int(self.get_home_ss()["turnovers"]) > 0:
            self.rat = round(int(self.get_home_ss()["assists"])/int(self.get_home_ss()["turnovers"]), 2)
        else:
            self.rat = int(self.get_home_ss()["assists"])

    def get_ratio_assists_turnovers(self):
        return self.rat

    def set_ratio_steals_turnovers(self):
        """Method which returns ratio steals / turnovers"""
        if int(self.get_home_ss()["turnovers"]) > 0:
            self.rst = round(int(self.get_home_ss()["steals"])/int(self.get_home_ss()["turnovers"]), 2)
        else:
            self.rst = int(self.get_home_ss()["steals"])

    def get_ratio_steals_turnovers(self):
        return self.rst

    def set_ts(self):
        """Method which returns the True Shoot %"""
        hss = self.get_home_ss()
        tci = int(hss["t2p_int"]) + int(hss["t3p_int"])
        ptos = int(hss["t2p_conv"]) * 2 + int(hss["t3p_conv"]) * 3 + int(hss["tl_conv"])
        self.ts = round((ptos / (2 * (tci + 0.44 * int(hss["tl_int"])))) * 100, 2)

    def get_ts(self):
        return self.ts

    def set_ortg(self):
        """Method which returns the Offensive Rating of a Team"""
        hss = self.get_home_ss()
        ptos = int(hss["t2p_conv"]) * 2 + int(hss["t3p_conv"]) * 3 + int(hss["tl_conv"])
        self.ortg = round((ptos/self.get_possessions())*100, 2)

    def get_ortg(self):
        return self.ortg

    def set_drtg(self):
        """Method which returns the Defensive Rating of a Team"""
        opp = self.get_away_ss()
        ptos = int(opp["t2p_conv"]) * 2 + int(opp["t3p_conv"]) * 3 + int(opp["tl_conv"])
        self.drtg = round((ptos / self.get_possessions()) * 100, 2)

    def get_drtg(self):
        return self.drtg

    def set_nrtg(self):
        """Method which returns the Net Rating of a Team"""
        self.nrtg = round(self.get_ortg() - self.get_drtg(), 2)

    def get_nrtg(self):
        return self.nrtg
