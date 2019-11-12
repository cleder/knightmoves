# -*- coding: utf-8 -*-
"""
Tests
"""
import json


class Game:

    def __init__(self):
        """Set up board."""
        self.items = []
        self.items.append(Item('Axe', [2, 2], attack=2))
        self.items.append(Item('Dagger', [2, 5], attack=1))
        self.items.append(Item('MagicStaff', [5, 2], attack=1, defence=1))
        self.items.append(Item('Helmet', [5, 5], defence=1))
        self.knights = {}
        self.knights['R'] = Knight('Red', [0, 0])
        self.knights['B'] = Knight('Blue', [7, 0])
        self.knights['G'] = Knight('Green', [7, 7])
        self.knights['Y'] = Knight('Yellow', [0, 7])

    def items_on_position(self, pos):
        return [item for item in self.items if item.position == pos and not item.equipped]

    def choose_best_item(self, items):
        for item in items:
            for char in ('A', 'M', 'D', 'H'): # hacky, item should have a weight
                if item.name.startswith(char):
                    return item

    def get_other_knight_on_position(self, pos, myknight):
        for knight in self.knights.values():
            if knight == myknight:
                continue
            if knight.position == pos and knight.status == 'alive':
                return knight
        return None

    def fight(self, knight, enemy):
        if knight.attack + .5 > enemy.defence:  # 0.5 surprise guarantees we never have a draw
            enemy.die()
        else:
            knight.die()

    def move(self, knight_key, direction):
        knight = self.knights[knight_key]
        pos = knight.move(direction)
        if not pos:
            # drowned or dead
            return
        items =  self.items_on_position(pos)
        item = self.choose_best_item(items)
        if not knight.item and item:
            knight.pickup_item(item)
        enemy = self.get_other_knight_on_position(pos, knight)
        if enemy:
            self.fight(knight, enemy)

    def get_state(self):
        """Return current state of the board."""
        state = {}
        for knight in self.knights.values():
            state[knight.color] = knight.get_state()
        for item in self.items:
            state[item.name] = item.get_state()
        return state

    def to_json(self):
        """Output game as json."""
        return json.dumps(self.get_state())

    def read_moves_from_file(self, filename):
        with open(filename, 'r') as f:
            assert f.readline().strip() == 'GAME-START'
            while True:
                try:
                    k, v = f.readline().strip().split(':')
                    self.move(k,v)
                except ValueError:
                    break


class Item:
    """"""
    def __init__(self, name, position, attack=0, defence=0, max_xy=None):
        """Initialize items."""
        if max_xy is None:
            max_xy = (7, 7)
        assert isinstance(position, list)
        assert len(position) == 2
        for i in [0, 1]:
            assert 0 <= position[i] <= max_xy[i]
        self.position = position
        self.name = name
        self.knight = None
        self.attack = attack
        self.defence = defence

    @property
    def equipped(self):
        return self.knight is not None

    def get_state(self):
        return [self.position, self.equipped]


class Knight:
    """"""

    def __init__(self, color, position, status='alive', max_xy=None):
        """Initialize knight."""
        if max_xy is None:
            max_xy = (7,7)
        assert isinstance(position, (tuple, list))
        assert len(position) == 2
        for i in [0,1]:
            assert 0 <= position[i] <= max_xy[i]
        self._position = position
        assert status in ['alive', 'dead', 'drowned']
        self._status = status
        self._color = color
        self._item = None
        self._defence = 1
        self._attack = 1

    def move(self, direction):
        """Move knight by one field."""
        if not self.position:
            return None
        if not self.status == 'alive':
            return None
        assert direction in ['N', 'S', 'E', 'W']
        moves = {
            'N': (-1, 0),
            'S': (1, 0),
            'W': (0, -1),
            'E': (0, 1),
        }
        _position = [self._position[0] + moves[direction][0], self._position[1] + moves[direction][1]]
        for i in [0, 1]:
            if not 0 <= _position[i] <= 7:
                self._status = 'drowned'
                self._position = None
                self.drop_item()
                return _position

        self.position = _position
        return _position

    def die(self):
        self.drop_item()
        self._status = 'dead'

    def drop_item(self):
        if self._item:
            self._item.knight = None
        self._item = None

    def pickup_item(self, item):
        assert item.position == self.position
        self._item = item
        item.knight = self

    @property
    def status(self):
        return self._status

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position
        if self.item:
            self.item.position = new_position

    @property
    def item(self):
        return self._item

    @property
    def defence(self):
        if self._item:
            return self._defence + self._item.defence
        return self._defence

    @property
    def attack(self):
        if self._item:
            return self._attack + self._item.attack
        return self._attack

    @property
    def color(self):
        return self._color

    def get_state(self):
        return [self.position,  self.status, self.item, self.attack, self.defence]