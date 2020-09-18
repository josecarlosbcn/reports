from decimal import Decimal, InvalidOperation
from constants import BCOLORS

"""Class to let us to calculate the advanced stats of a player for a game"""


class PlayerAS(object):
    def __init__(self, stats, team_stats, opp_stats, team_possessions):
        self.name = None
        self.number = None
        self.game_score = 0
        self.dre = 0
        self.per = 0
        self.ts_percentage = 0
        self.usg_percentage = 0
        self.total_reb_percentage = 0
        self.total_reb_def_percentage = 0
        self.total_reb_of_percentage = 0
        self.steals_percentage = 0
        self.effective_field_goal_percentage = 0
        self.assists_percentage = 0
        self.assists_per_turnover = 0
        self.assists_ratio = 0
        self.ortg = 0
        self.drtg = 0
        self.nrtg = 0
        self.set_name(stats)
        self.set_number(stats)
        self.set_standard_stats(stats)
        self.set_team_stats(team_stats)
        self.set_opp_team_stats(opp_stats)
        self.set_team_possessions(team_possessions)
        self.make_calculus()

    def make_calculus(self):
        self.set_game_score()
        self.set_dre()
        self.set_per()
        self.set_ts_percentage()
        self.set_usg_percentage()
        self.set_total_reb_percentage()
        self.set_total_reb_def_percentage()
        self.set_total_reb_of_percentage()
        self.set_steals_percentage()
        self.set_effective_field_goal_percentage()
        self.set_assists_percentage()
        self.set_assists_per_turnover()
        self.set_assists_ratio()
        self.set_defensive_ratio()
        self.set_offensive_ratio()
        self.set_net_ratio()

    """Setters & Getters"""
    def set_name(self, stats):
        self.name = stats["name"]

    def get_name(self):
        return self.name

    def set_number(self, stats):
        self.number = stats["numero"]

    def get_number(self):
        return self.number

    def set_standard_stats(self, stats):
        self.standard_stats = stats

    def get_standard_stats(self):
        return self.standard_stats

    def set_team_stats(self, team_stats):
        self.team_stats = team_stats

    def get_team_stats(self):
        return self.team_stats

    def set_opp_team_stats(self, opp_team_stats):
        self.opp_team_stats = opp_team_stats

    def get_opp_team_stats(self):
        return self.opp_team_stats

    def set_team_possessions(self, poss):
        self.team_possessions = poss

    def get_team_possessions(self):
        return self.team_possessions

    def set_game_score(self):
        """Method which calculus game score through pss (player standard stats)"""
        bx = self.get_standard_stats()
        tcInt = bx["t2p_int"] + bx["t3p_int"]
        tcConv = bx["t2p_conv"] + bx["t3p_conv"]
        ft = bx["tl_int"] - bx["tl_conv"]
        ptos = bx["t2p_conv"]*2 + bx["t3p_conv"]*3 + bx["tl_conv"]
        #Con "%.2f" %  round(x, 2) además de redondear a dos decimales, nos quedamos con los ceros finales
        result = "%.2f" % round(float(ptos) + (float(0.4)*float(tcConv)) - (float(0.7)*float(tcInt)) - (float(0.4)*float(ft)) + (float(0.7)*float(bx["reb_of"]))
        + (float(0.3)*float(bx["reb_def"])) + float(bx["steals"]) + (float(0.7)*float(bx["assists"])) + (float(0.7)*float(bx["block_shots"]))
        - (float(0.4)*float(bx["fouls_cm"])) - float(bx["turnovers"]), 2)
        self.game_score = "%.2f" % round(Decimal(result)/bx["games"], 2)

    def get_game_score(self):
        return self.game_score

    def set_dre(self):
        """Method which calculate DRE metric"""
        bx = self.get_standard_stats()
        ptos = float(bx["t2p_conv"]*2 + bx["t3p_conv"]*3 + bx["tl_conv"])
        fga = float(bx["t2p_int"] + bx["t3p_int"])
        trb = float(bx["reb_def"] + bx["reb_of"])
        d1 = ptos + (0.2*trb) + (1.7*float(bx["steals"])) + (0.535*float(bx["block_shots"])) + (0.5*float(bx["assists"]))
        d2 = (0.9*fga) + (0.35*float(bx["tl_int"])) + (1.4*float(bx["turnovers"])) + (0.136*float(bx["minutes"]))
        result = "%.2f" % round(d1-d2, 2)
        self.dre = "%.2f" % round(Decimal(result)/bx["games"], 2)

    def get_dre(self):
        return self.dre

    def set_per(self):
        self.per = 0.0

    def get_per(self):
        return self.per

    def set_ts_percentage(self):
        """Method which calculates TS Percentage metric for a player"""
        bx = self.get_standard_stats()
        ptos = float(bx["t2p_conv"]*2 + bx["t3p_conv"]*3 + bx["tl_conv"])
        tcInt = float(bx["t2p_int"] + bx["t3p_int"])
        tsAttempts = float(tcInt + (0.44*float(bx["tl_int"])))
        result = 0.00
        if tsAttempts > 0.00:
            result = (ptos/(2*tsAttempts))*100
        self.ts_percentage = "%.2f" % round(result, 2)

    def get_ts_percentage(self):
        return self.ts_percentage

    def set_usg_percentage(self):
        """Method which calculate USG% for each player from each team"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        tcInt = bx["t2p_int"] + bx["t3p_int"]
        a = tcInt + (Decimal('0.44')*bx["tl_int"]) + bx["turnovers"]
        b = team["minutes"]/5
        c = (team["t2p_int"] + team["t3p_int"]) + (Decimal('0.44')*team["tl_int"]) + team["turnovers"]
        result = 0.00
        if bx["minutes"] > 0:
            result = ((Decimal(a)*Decimal(b))/(bx["minutes"]*c))*100
        self.usg_percentage = "%.2f" % round(result, 2)

    def get_usg_percentage(self):
        return self.usg_percentage

    def set_total_reb_percentage(self):
        """Method which calculate Total Rebound Percentage"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        player_rebounds = bx["reb_def"] + bx["reb_of"]
        team_rebounds = team["reb_def"] + team["reb_of"]
        opp_team_rebounds =  opp_team["reb_def"] + opp_team["reb_of"]
        result = 0.00
        try:
            if bx["minutes"] > 0 and bx["minutes"] > 0:
                result = ((player_rebounds * (team["minutes"]/5)) / (bx["minutes"] * (team_rebounds + opp_team_rebounds)))*100
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
        except InvalidOperation:
            print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)

        self.total_reb_percentage = "%.2f" % round(result, 2)

    def get_total_reb_percentage(self):
        return self.total_reb_percentage

    def set_total_reb_def_percentage(self):
        """Method which calculate Total Rebound Defensive Percentage"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        result = 0.00
        try:
            if bx["minutes"] > 0 and bx["minutes"] > 0:
                result = ((bx["reb_def"] * (team["minutes"]/5)) / (bx["minutes"] * (team["reb_def"] + opp_team["reb_of"])))*100
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
        except InvalidOperation:
            print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)

        self.total_reb_def_percentage = "%.2f" % round(result, 2)

    def get_total_reb_def_percentage(self):
        return self.total_reb_def_percentage

    def set_total_reb_of_percentage(self):
        """Method which calculate Total Rebound Ofensive Percentage"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        result = 0.00
        try:
            if bx["reb_of"] > 0 and bx["minutes"] > 0:
                result = ((bx["reb_of"] * (team["minutes"]/5)) / (bx["minutes"] * (team["reb_of"] + opp_team["reb_def"])))*100
        except ZeroDivisionError:
            print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
        self.total_reb_of_percentage = "%.2f" % round(result, 2)

    def get_total_reb_of_percentage(self):
        return self.total_reb_of_percentage

    def set_steals_percentage(self):
        """Method which calculate Steals Percentage of a player"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        poss = self.get_team_possessions()
        result = 0.00
        if bx["minutes"] > 0:
            result = ((bx["steals"] * (team["minutes"]/Decimal('5'))) / Decimal(float(bx["minutes"]) * poss)) * 100
        self.steals_percentage = "%.2f" % round(result, 2)

    def get_steals_percentage(self):
        return self.steals_percentage

    def set_effective_field_goal_percentage(self):
        """Method which calculate Effective Field Goal (eTC) of a player"""
        bx = self.get_standard_stats()
        tcInt = float(bx["t2p_int"] + bx["t3p_int"])
        tcConv = float(bx["t2p_conv"] + bx["t3p_conv"])
        result = 0.00
        if tcInt > 0:
            result = ((tcConv + (0.5 * float(bx["t3p_conv"]))) / tcInt) * 100
        self.effective_field_goal_percentage = "%.2f" % round(result, 2)

    def get_effective_field_goal_percentage(self):
        return self.effective_field_goal_percentage

    def set_assists_percentage(self):
        """Method which calculate Assists Percentage of a player"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        team_tc_conv = team["t2p_conv"] + team["t3p_conv"]
        player_tc_conv = bx["t2p_conv"] + bx["t3p_conv"]
        result = 0.00
        try:
            if bx["minutes"] > 0:
                result = (bx["assists"] / (((bx["minutes"] / (team["minutes"] / 5)) * team_tc_conv) - player_tc_conv))*100
                result = result if result <= 100 and result >= 0 else 0
        except ZeroDivisionError:
            print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
        except InvalidOperation:
            print(BCOLORS.WARNING + "Error: Invalid Operation" + BCOLORS.ENDC)

        self.assists_percentage = "%.2f" % round(result, 2)

    def get_assists_percentage(self):
        return self.assists_percentage

    def set_assists_per_turnover(self):
        """Method which calculate Ratio Assists Per Turnover of a player"""
        bx = self.get_standard_stats()
        ratio = bx["assists"]
        if bx["turnovers"] > 0:
            ratio = bx["assists"] / bx["turnovers"]
        self.assists_per_turnover = "%.2f" % round(ratio, 2)

    def get_assists_per_turnover(self):
        return self.assists_per_turnover

    def set_assists_ratio(self):
        """Method which calculate Assists Ratio of a player"""
        bx = self.get_standard_stats()
        tcInt = float(bx["t2p_int"] + bx["t3p_int"])
        denominador = tcInt + (0.44 * float(bx["tl_int"])) + float(bx["assists"]) +float(bx["turnovers"])
        numerador = float(bx["assists"])
        result = 0.00
        if denominador > 0:
            result = (numerador / denominador) * 100
        self.assists_ratio = "%.2f" % round(result, 2)

    def get_assists_ratio(self):
        return self.assists_ratio

    def set_defensive_ratio(self):
        """Method which calculate Defensive Ratio of a player. The total points received in
        100 possessions"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        if bx["minutes"] > 0:
            opp_fga = opp_team["t2p_int"] + opp_team["t3p_int"]
            opp_fgm = opp_team["t2p_conv"] + opp_team["t3p_conv"]
            try:
                dor = Decimal(opp_team["reb_of"] / (opp_team["reb_of"] + team["reb_def"]))
            except ZeroDivisionError:
                print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
                dor = 0
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                dor = 0

            try:
                dfg = Decimal(opp_fgm / opp_fga)
            except ZeroDivisionError:
                print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
                dfg = 0
            try:
                fmwt = Decimal((dfg * (1 - dor)) / (dfg * (1 - dor) + (1 - dfg) * dor))
            except:
                fmwt = 0
            stops1 = bx["steals"] + bx["block_shots"] * fmwt * (1 - Decimal('1.07') * dor) + bx["reb_def"] * (1 - fmwt)

            try:
                stops2 = (Decimal((opp_fga - opp_fgm - team["block_shots"]) / team["minutes"]) * fmwt * (1 - Decimal('1.07') * dor) + Decimal((opp_team["turnovers"] - team["steals"]) / team["minutes"])) * bx["minutes"] + Decimal(bx["fouls_cm"] / team["fouls_cm"]) * Decimal('0.4') * opp_team["tl_int"] * (1 - Decimal(opp_team["tl_conv"] / opp_team["tl_int"]))**2
            except ZeroDivisionError:
                print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
                stops2 = 0
            except InvalidOperation:
                print(BCOLORS.WARNING + "Error: Invalid Operation" + BCOLORS.ENDC)
                stops2 = 0

            stops = stops1 + stops2
            poss = self.get_team_possessions()
            if bx["minutes"] > 0:
                stop_percentage = (float(stops) * float(opp_team["minutes"])) / (float(poss) * float(bx["minutes"]))
            else:
                stop_percentage = 0.00
            opp_points = opp_team["t2p_conv"] * 2 + opp_team["t3p_conv"] * 3 + opp_team["tl_conv"]
            team_defensive_rating = 100 * (float(opp_points) / poss)
            try:
                d_pts_per_scposs = float(opp_points) / (float(opp_fgm) + (1 - (1 - (float(opp_team["tl_conv"]) / float(opp_team["tl_int"])))**2) * float(opp_team["tl_int"])*0.4)
                result = Decimal(team_defensive_rating) + Decimal('0.2') * (100 * Decimal(d_pts_per_scposs) * (1 - Decimal(stop_percentage)) - Decimal(team_defensive_rating))
            except ZeroDivisionError:
                print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
                d_pts_per_scposs = 0
                result = 0.00



            # print("dor: " + str(dor))
            # print("dfg: " + str(dfg))
            # print("fmwt: " + str(fmwt))
            # print("stops1: " + str(stops1))
            # print("stops2: " + str(stops2))
            # print("stops: " + str(stops))
            # print("poss: " + str(poss))
            # print("stop_percentage: " + str(stop_percentage))
            # print("opp_points: " + str(opp_points))
            # print("team_defensive_rating: " + str(team_defensive_rating))
            # print("d_pts_per_scposs: " + str(d_pts_per_scposs))
            # print("drtg: " + str(result) + "\n")
        else:
            result = 0.00
        self.drtg = "%.2f" % round(result, 2)

    def get_defensive_ratio(self):
        return self.drtg

    def set_offensive_ratio(self):
        """Method which calculate Offensive Ratio of a player. The total points scored in
        100 possessions"""
        bx = self.get_standard_stats()
        team = self.get_team_stats()
        opp_team = self.get_opp_team_stats()
        if bx["minutes"] > 0 and (bx["t2p_int"] + bx["t3p_int"]) > 0:
            fgm = bx["t2p_conv"] + bx["t3p_conv"]
            fga = bx["t2p_int"] + bx["t3p_int"]
            team_fgm = team["t2p_conv"] + team["t3p_conv"]
            team_fga = team["t2p_int"] + team["t3p_int"]
            team_points = team["t2p_conv"]*2 + team["t3p_conv"]*3 + team["tl_conv"]
            points = bx["t2p_conv"]*2 + bx["t3p_conv"]*3 + bx["tl_conv"]

            try:
                qAST = (Decimal(bx["minutes"] / (team["minutes"] / 5)) * (Decimal('1.14') * Decimal((team["assists"] - bx["assists"]) / team_fgm))) + \
                       Decimal((((team["assists"] / team["minutes"]) * bx["minutes"] * 5 - bx["assists"]) / ((team_fgm / team["minutes"]) * bx["minutes"] * 5 - fgm)) * (1 - (bx["minutes"] / (team["minutes"] / 5))))
            except ZeroDivisionError:
                print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
                qAST = 1
            except InvalidOperation:
                print(BCOLORS.WARNING + "Error: Invalid Operation" + BCOLORS.ENDC)
                qAST = 1

            fg_part = fgm * (1 - Decimal('0.5') * Decimal((points - bx["tl_conv"]) / (2 * fga)) * qAST)

            try:
                ast_part = Decimal('0.5') * Decimal(((team_points - team["tl_conv"]) - (points - bx["tl_conv"])) / (2*(team_fga - fga))) * bx["assists"]
            except ZeroDivisionError:
                print(BCOLORS.WARNING + "Error: División por cero" + BCOLORS.ENDC)
                ast_part = 0

            if bx["tl_int"] > 0:
                ft_part = Decimal(1 - (1 - (bx["tl_conv"] / bx["tl_int"]))**2) * Decimal('0.4') * bx["tl_int"]
            else:
                ft_part = 0
            team_scoring_poss = Decimal(team_fgm + Decimal(1 - (1 - (team["tl_conv"] / team["tl_int"]))**2) * team["tl_int"] * Decimal('0.4'))
            try:
                team_orb_percentage = Decimal(team["reb_of"] / (team["reb_of"] + ((opp_team["reb_def"] + opp_team["reb_of"]) - opp_team["reb_of"])))
            except ZeroDivisionError:
                print(BCOLORS.FAIL + "Error: División por cero" + BCOLORS.ENDC)
                team_orb_percentage = 0
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                team_orb_percentage = 0

            team_play_percentage = Decimal(team_scoring_poss / (team_fga + team["tl_int"] * Decimal('0.4') + team["turnovers"]))
            try:
                team_orb_weight = ((1 - team_orb_percentage) * team_play_percentage) / ((1 - team_orb_percentage) * team_play_percentage + team_orb_percentage * (1 - team_play_percentage))
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                team_orb_weight = 0

            orb_part = bx["reb_of"] * team_orb_weight * team_play_percentage

            fg_x_poss = (fga - fgm) * (1 - Decimal('1.07') * team_orb_percentage)
            if bx["tl_conv"] > 0:
                ft_x_poss = Decimal((1 - (bx["tl_conv"] / bx["tl_int"]))**2) * Decimal('0.4') * bx["tl_int"]
            else:
                ft_x_poss = Decimal(1 - (bx["tl_conv"] / 1)**2) * Decimal('0.4') * bx["tl_int"]
            try:
                sc_poss = (fg_part + ast_part + ft_part) * (1 - (team["reb_of"] / team_scoring_poss) * team_orb_weight * team_play_percentage) + orb_part
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                sc_poss =0

            tot_poss = sc_poss + fg_x_poss + ft_x_poss + bx["turnovers"]

            pprod_fg_part = 2 * (fgm + Decimal('0.5') * bx["t3p_conv"]) * (1 - Decimal('0.5') * Decimal((points - bx["tl_conv"]) / (2 * fga)) * qAST)

            try:
                pprod_ast_part = 2 * ((team_fgm - fgm + Decimal('0.5') * (team["t3p_conv"] - bx["t3p_conv"])) / (team_fgm - fgm)) * Decimal('0.5') * Decimal(((team_points - team["tl_conv"]) - (points - bx["tl_conv"])) / (2 * (team_fga - fga))) * bx["assists"]
            except:
                pprod_ast_part = 0

            pprod_orb_part = bx["reb_of"] * team_orb_weight * team_play_percentage * (team_points / (team_fgm + Decimal(1 - (team["tl_conv"] / team["tl_int"])**2) * Decimal('0.4') * team["tl_int"]))
            try:
                pprod = (pprod_fg_part + pprod_ast_part + bx["tl_conv"]) * (1 - (team["reb_of"] / team_scoring_poss) * team_orb_weight * team_play_percentage) + pprod_orb_part
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                pprod = 0

            try:
                result = 100 * (pprod / tot_poss)
            except InvalidOperation:
                print(BCOLORS.FAIL + "Error: Invalid Operation" + BCOLORS.ENDC)
                result = 0

            # print("fgm: " + str(fgm))
            # print("fga: " + str(fga))
            # print("team_fgm: " + str(team_fgm))
            # print("team_fga: " + str(team_fga))
            # print("team_points: " + str(team_points))
            # print("points: " + str(points))
            # print("qAST: " + str(qAST))
            # print("fg_part: " + str(fg_part))
            # print("ast_part: " + str(ast_part))
            # print("ft_part: " + str(ft_part))
            # print("team_scoring_poss: " + str(team_scoring_poss))
            # print("team_orb_percentage: " + str(team_orb_percentage))
            # print("team_play_percentage: " + str(team_play_percentage))
            # print("team_orb_weight: " + str(team_orb_weight))
            # print("orb_part: " + str(orb_part))
            # print("fg_x_poss: " + str(fg_x_poss))
            # print("ft_x_poss: " + str(ft_x_poss))
            # print("sc_poss: " + str(sc_poss))
            # print("tot_poss: " + str(tot_poss))
            # print("pprod_fg_part: " + str(pprod_fg_part))
            # print("pprod_ast_part: " + str(pprod_ast_part))
            # print("pprod_orb_part: " + str(pprod_orb_part))
            # print("pprod: " + str(pprod))
            # print("result: " + str(result) + "\n")
        else:
            result = 0.00

        self.ortg = "%.2f" % round(result, 2)
        if Decimal(self.ortg) < 0 or Decimal(self.ortg) >= 1000:
            """For one game, maybe we've got a negative result or one so big, so, for just only a game, we get the ORTG 
            using team's formula"""
            print(BCOLORS.OKBLUE + "ORTG negativo o superior a 1000 para jugadora => recalculamos a través de la fórmula de equipo" + BCOLORS.ENDC)
            bx = self.get_standard_stats()
            result = round((bx["t2p_conv"]*2 + bx["t3p_conv"]*3 + bx["tl_conv"])/self.get_team_possessions(), 2)
            self.ortg = "%.2f" % result

    def get_offensive_ratio(self):
        return self.ortg

    def set_net_ratio(self):
        # if self.get_offensive_ratio() == 0.00 or self.get_defensive_ratio() == 0.00:
        #     self.set_offensive_ratio(player, team, opp_team)
        #     self.set_defensive_ratio(player, team, opp_team)
        self.nrtg = "%.2f" % round(float(self.get_offensive_ratio()) - float(self.get_defensive_ratio()), 2)

    def get_net_ratio(self):
        return self.nrtg
