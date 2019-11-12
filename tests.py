import json
import unittest


from knightmoves import Game, Knight, Item

class KnightTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_drop_item(self):
        knight = Knight('Red', [2, 2])
        item = Item('Helmet', [2, 2], defence=1)
        item.knight = knight
        assert item.equipped # should have its own test
        knight._item = item
        assert knight.attack == 1 # For brevity should have its own test
        assert knight.defence == 2
        knight.drop_item()
        assert knight.item is None
        assert item.knight is None
        assert item.position == knight.position
        assert not item.equipped

    def test_pickup_item(self):
        knight = Knight('Red', [2, 2])
        item = Item('Helmet', [2, 2], defence=1)
        assert not item.equipped

        knight.pickup_item(item)

        assert item.equipped
        assert knight.item == item
        assert item.knight == knight
        assert item.position == knight.position

    def test_drown(self):
        knight = Knight('Red', [0, 0])
        knight.move('N')
        assert knight.status == 'drowned'
        assert knight.position is None

        knight = Knight('Red', [0, 0])
        knight.move('W')
        assert knight.status == 'drowned'
        assert knight.position is None

        knight = Knight('Red', [7, 7])
        knight.move('S')
        assert knight.status == 'drowned'
        assert knight.position is None

        knight = Knight('Red', [7, 7])
        knight.move('E')
        assert knight.status == 'drowned'
        assert knight.position is None

    def test_drown_drops_item_on_last_position(self):
        knight = Knight('Red', [0, 0])
        item = Item('Helmet', [0, 0], defence=1)
        knight.pickup_item(item)
        knight.move('N')
        assert item.position == [0, 0]
        assert not item.equipped


class GameTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.initial_expected = {
          "Red": [
            [
              0,
              0
            ],
            "alive",
            None,
            1,
            1
          ],
          "Blue": [
            [
              7,
              0
            ],
            "alive",
            None,
            1,
            1
          ],
          "Green": [
            [
              7,
              7
            ],
            "alive",
            None,
            1,
            1
          ],
          "Yellow": [
            [
              0,
              7
            ],
            "alive",
            None,
            1,
            1
          ],
          "Axe": [
            [
              2,
              2
            ],
            False,
          ],
          "Dagger": [
            [
              2,
              2
            ],
            False,
          ],
          "MagicStaff": [
            [
              2,
              2
            ],
            False,
          ],
          "Helmet": [
            [
              2,
              2
            ],
            False,
          ]
        }


    def test_init_state(self):
        game = Game()
        assert game.get_state() == self.initial_expected

    def test_init_game_json(self):
        game = Game()
        assert json.loads(game.to_json()) == self.initial_expected


if __name__ == '__main__':
    unittest.main()
