# -*- coding: UTF-8 -*-
# gamebody.py
import basic
from basic import *
from map_info import *
import command

from custom_json import *
from copy import deepcopy
from random import choice, shuffle

STATE_CONTINUE = -1
STATE_TIE = 2

def default_judge(game, events):
    dead_bases = 0
    rst = None
    for element in game.map_info.elements.values():
        if element.kind == BASE and element.health <= 0:
            dead_bases += 1
            rst = 1 - element.team
    if dead_bases == 1:
        return rst
    if game.round >= game.max_round or dead_bases == 2:
        return 0 if game.score(0) > game.score(1) else (1 if game.score(1) > game.score(0) else STATE_TIE)
    return STATE_CONTINUE


def compare_commands(l_command, r_command):
    """return whether l_command should be executed first"""
    sequence_list = ['Produce', 'Attack', 'Supply', 'Fix', 'ChangeDest']
    l_type = l_command.__class__.__name__
    if l_type.startswith('Attack'):
        l_type = 'Attack'
    r_type = r_command.__class__.__name__
    if r_type.startswith('Attack'):
        r_type = 'Attack'
    if sequence_list.index(l_type) < sequence_list.index(r_type):
        return -1
    elif sequence_list.index(l_type) > sequence_list.index(r_type):
        return 1
    else:
        return choice([-1, 1])

def compare_speed(l_tuple, r_tuple):
    if l_tuple[1] > r_tuple[1]:
        return 1
    elif l_tuple[1] < r_tuple[1]:
        return -1
    else:
        return choice([-1, 1])

class GameBody(object):
    """docstring for GameBody"""
    def __init__(self, map_info, judge=default_judge, **kwargs):
        self.map_info = map_info
        self.round = 0
        self.scores = [0, 0]
        self.populations = [sum([element.population for element in self.elements(0).values() if element.population != None]),
                            sum([element.population for element in self.elements(1).values() if element.population != None])]
        self.production_lists = [[], []]
        self.commands = [[], []]
        self.state = STATE_CONTINUE
        for kw in ['round', 'scores', 'production_lists', 'commands', "state"]:
            if kw in kwargs:
                setattr(self, kw, kwargs[kw])
        self.round = max(self.round, 0)         # in case round < 0
        self.scores = [max(score, 0) for score in self.scores]      # in case score < 0

        self.judge = judge

    @property
    def map(self):
        return self.map_info.types

    @property
    def max_population(self):
        return self.map_info.max_population

    @property
    def max_round(self):
        return self.map_info.max_round

    @property
    def record_interval(self):
        return self.map_info.record_interval

    @property
    def time_per_round(self):
        return self.map_info.time_per_round

    @property
    def weather(self):
        return self.map_info.weather

    def score(self, team):
        """return score of the team"""
        return self.scores[team]

    def elements(self, team):
        """return elements of the team"""
        our_elements = {}
        for index, element in self.map_info.elements.items():
            if isinstance(element, UnitBase) and element.team == team:
                our_elements[index] = element
        return our_elements

    def vision(self, team):
        """shared 3-level vision of the whole team"""
        vision = [[], [], []]
        for level in xrange(3):
            for element in self.elements(team).values():
                if element.kind == SCOUT:
                    vision[level].extend(element.pos.region(level, 
                        max(0, element.sight_ranges[level])))
                else:
                    vision[level].extend(element.pos.region(level, 
                        max(0, element.sight_ranges[level] + self.map_info.weather)))
            vision[level] = set(vision[level])
            tmp = []
            for point in vision[level]:
                if point.inMap(self.map_info):
                    tmp.append(point)
            vision[level] = set(tmp)
        return vision

    def view_elements(self, perspective):
        """return a dict containing all the elements in team vision"""
        can_see = {}
        vision = self.vision(perspective)
        for index, element in self.map_info.elements.items():
            if element.kind == BASE or element.kind == FORT or element.kind == MINE or element.kind == OILFIELD:
                tmp = deepcopy(element)
                setattr(tmp, 'visible', False)        # in fact, this element is not in sight
                can_see[index] = tmp.globalGhost()
            for point in element.pos.region(element.level, 0):
                if point in vision[element.level]:
                    if hasattr(element, 'team') is False or element.team != perspective:     # 非己方
                        can_see[index] = element.ghost()
                    else:
                        can_see[index] = element
                    break
        return can_see

    def production_list(self, team):
        """return current production list of the team"""
        return  self.production_lists[team]

    def population(self, team):
        """return total population of the team"""
        return self.populations[team]

    def set_command(self, team, cmd):
        """add a command and resolve conflicts"""
        if isinstance(cmd, command.Produce):
            return cmd.add_to(team, self)
        operator = self.map_info.elements.get(cmd.operand)
        if operator is None:
            return False
        if not isinstance(operator, UnitBase) or team != operator.team:
            return False
        return cmd.add_to(self)

    def run(self):
        """run one round and return the events took place"""
        self.round = self.round + 1
        events = []
        # sort commands
        all_commands = self.commands[0] + self.commands[1]
        all_commands.sort(cmp = compare_commands)
        for cmd in all_commands:
                events += cmd.result_event(self)
        elements = self.map_info.elements
        l = [(element.index, element.speed) for element in elements.values()
                    if hasattr(element, 'speed') and element.speed != None]
        l.sort(cmp = compare_speed)
        for item in l:
            events += elements[item[0]].move(self)
        # update production_lists and create new elements
        for team_index in [0, 1]:
            production_list = self.production_lists[team_index]
            out_entry = []
            for entry in production_list:
                entry[1] -= 1 if entry[1] > 0 else 0
                if (entry[1] == 0 and
                    self.populations[team_index] + PROPERTY[entry[0]]['population'] <= self.max_population):
                    for element in elements.values():
                        if element.kind == BASE and element.team == team_index:
                            if entry[0] == SUBMARINE:
                                check_region = [point for point in element.pos.region(level = UNDERWATER, range = 1) if element.pos.distance(point) == 1 and
                                                                                                                        point.x >= 0 and point.x < self.map_info.x_max and
                                                                                                                        point.y >= 0 and point.y < self.map_info.y_max]
                            elif entry[0] == FIGHTER or entry[0] == SCOUT:
                                check_region = element.pos.region(level = AIR, range = 0)
                            else:
                                check_region = [point for point in element.pos.region(level = SURFACE, range = 1) if element.pos.distance(point) == 1 and
                                                                                                                     point.x >= 0 and point.x < self.map_info.x_max and
                                                                                                                     point.y >= 0 and point.y < self.map_info.y_max]
                            shuffle(check_region)
                            for point in check_region:
                                if self.map_info.element(point) == None:
                                    if entry[0] == FIGHTER or entry[0] == SCOUT or self.map_info.map_type(point.x, point.y) == OCEAN:
                                        out_entry.append(entry)
                                        class_name = {SUBMARINE: 'Submarine', DESTROYER: 'Destroyer', CARRIER: 'Carrier', 
                                                      CARGO: 'Cargo', FIGHTER: 'Fighter', SCOUT: 'Scout'}[entry[0]]
                                        class_ = getattr(basic, class_name)
                                        new_element = class_(team_index, point)
                                        dead_index = [event.index for event in events if isinstance(event, Destroy)]
                                        index = self.map_info.add_element(new_element, dead_index)
                                        self.populations[team_index] += new_element.population
                                        events.append(Create(index, entry[0], point))
                                        new_element.fuel = 1 if isinstance(new_element, Plane) else 0
                                        if new_element.kind == CARGO:
                                            new_element.metal = 0
                                            events += element.supply(new_element, fuel=new_element.fuel_max / 2, metal=0)
                                        else:
                                            events += element.supply(new_element, metal=0)
                                        break
                            break
            for item in out_entry:
                production_list.remove(item)
        # Fort score
        for element in self.map_info.elements.values():
            if element.kind == FORT and (element.team == 0 or element.team == 1):
                self.scores[element.team] += FORT_SCORE

        self.commands = [[], []]

        # Update state
        self.state = self.judge(self, events)

        return events

    def save(self, filename):
        """Save game to file"""
        open(filename).write(self.saves())

    def saves(self):
        """Save game to string"""
        # Hide judge from json encoder
        judge = self.judge
        del self.judge
        encoded_str = MyEncoder(sort_keys=True,
                                separators=(',', ':')).encode(self)
        self.judge = judge

        return encoded_str

def load(filename):
    """Read game from file"""
    return loads(open(filename).read())

def loads(game_str):
    """Read game from string"""
    game =  MyDecoder().decode(game_str)
    game.map_info.elements = {int(index_str): element for index_str, element in
                              game.map_info.elements.items()}
    return game
