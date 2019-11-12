# -*- coding: utf-8 -*-
"""


"""
import json


class Game:

    def __init__(self):
        """Set up board."""
        self.items = []
        self.items.append(Item('Axe', [2, 2], attack=2))
        self.items.append(Item('Dagger', [2, 2], attack=1))
        self.items.append(Item('MagicStaff', [2, 2], attack=1, defence=1))
        self.items.append(Item('Helmet', [2, 2], defence=1))
        self.knights = {}
        self.knights['R'] = Knight('Red', [0, 0])
        self.knights['B'] = Knight('Blue', [7, 0])
        self.knights['G'] = Knight('Green', [7, 7])
        self.knights['Y'] = Knight('Yellow', [0, 7])

    def move(self, knight_key, direction):
        knight = self.knights[knight_key]
        knight.move(direction)


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
        assert direction in ['N', 'S', 'E', 'W']
        moves = {
            'N': (-1, 0),
            'S': (1, 0),
            'W': (0, -1),
            'E': (0, 1),
        }
        _position = (self._position[0] + moves[direction][0], self._position[1] + moves[direction][1])
        for i in [0, 1]:
            if not 0 <= _position[i] <= 7:
                self._status = 'drowned'
                self._position = None
                self.drop_item()
                return _position

        if self.status != 'alive':
            pass

        self.position = _position
        return _position

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