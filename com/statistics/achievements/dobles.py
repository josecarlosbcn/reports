

class Doubles(object):
    def __init__(self, id_game):
        self.set_id_game(id_game)
        self.points = 0
        self.rebounds = 0
        self.assits = 0
        self.steals = 0
        self.block_shots = 0

    """Getters & Setters"""
    def set_id_player(self, id):
        self.id_player = id

    def get_id_player(self):
        return self.id_player

    def set_id_game(self, id):
        self.id_game = id

    def get_id_game(self):
        return self.id_game

    def set_points(self, points):
        self.points = points

    def get_points(self):
        return self.points

    def set_rebounds(self, rebounds):
        self.rebounds = rebounds

    def get_rebounds(self):
        return self.rebounds

    def set_assists(self, assists):
        self.assits = assists

    def get_assists(self):
        return self.assits

    def set_steals(self, steals):
        self.steals = steals

    def get_steals(self):
        return self.steals

    def set_block_shots(self, block_shots):
        self.block_shots = block_shots

    def get_block_shots(self):
        return self.block_shots
