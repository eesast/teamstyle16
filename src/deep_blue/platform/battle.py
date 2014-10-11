import copy
import logging
import json
import socket
from logic import map_info, gamebody

logger = logging.getLogger(__name__)

class Battle(object):
    def __init__(self, map_info):
        # Just check record_interval in map_info, because invalid interval
        # may casue run time error (e.g. modulo by zero)
        if map_info.record_interval <= 0:
            raise ValueError('record_interval should be positive integer')

        self.gamebody = gamebody.GameBody(map_info)
        self.history = {
            'score': [],
            'unit_num': [],
            'population': [],
            'command': []
        }
        self.key_frames = []

        self.record_history()
        self.record_key_frame()  # record beginning frame

    def map_info(self):
        return self.gamebody.map_info

    def team_name(self, team):
        return self.ais[team].team_name

    def round(self):
        return self.gamebody.round

    def status(self):
        return self.gamebody.status

    def score(self, team):
        return self.gamebody.score(team)

    def elements(self, team):
        return self.gamebody.elements(team)

    def vision(self, team):
        return self.gamebody.vision(team)

    def view_elements(self, perspective):
        return self.gamebody.view_elements(perspective)

    def production_list(self, team):
        return self.gamebody.production_list(team)

    def population(self, team):
        return self.gamebody.population(team)

    def score_history(self):
        return self.history['score']

    def unit_num_history(self):
        return self.history['unit_num']

    def population_history(self):
        return self.history['population']

    def command_history(self):
        return self.history['command']

    def set_command(self, team, command):
        return self.gamebody.set_command(team, command)

    def commands(self, team):
        return self.gamebody.commands[team]

    def next_round(self):
        """Advance the game to the next round, return events happened"""
        logger.info('Moving to the next round')

        self.record_commands()  # commands of this round become fixed
        events = self.gamebody.run()
        # Record history & key frame as early as possible, or infomation of
        # the last round will be lost (because no next_round will be called).
        self.record_history()
        if self.gamebody.round % self.gamebody.record_interval == 0:
            self.record_key_frame

        return events

    def save(filename):
        save_file = open(filename, 'w')
        contents = {
            'gamebody': self.gamebody.saves(),
            'history': self.history,
            'key_frames': self.key_frames
        }
        json.dump(save_file, contents, sort_keys=True, separators=(',', ':'))

    def record_history(self):
        history = self.history
        game = self.gamebody
        history['score'].append(copy.copy(game.scores))
        history['unit_num'].append([len(game.elements(0)),
                              len(game.elements(1))])
        history['population'].append(copy.copy(game.populations))

    def record_commands(self):
        history['command'].append(copy.copy(game.commands))

    def record_key_frame(self):
        frame = (copy.deepcopy(self.gamebody.elements),
                 copy.deepcopy(self.gamebody.production_list))
        self.key_frames.append(frame)

def load(filename):
    contents = json.load(filename)
    game = gamebody.loads(contents['gamebody'])
    battle = Battle(game.map_info)

    battle.gamebody = contents['gamebody']
    battle.history = contents['history']
    battle.key_frames = contents['key_frames']
