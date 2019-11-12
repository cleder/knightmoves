Only tested with python 3.6
Run the test with pytest
# Usage
```
>>> import knightmoves
>>> game = knightmoves.Game()
>>> game.read_moves_from_file('moves.txt')
>>> game.to_json()
'{"Red": [[2, 0], "alive", null, 1, 1], "Blue": [[7, 1], "alive", null, 1, 1], "Green": [[6, 7], "alive", null, 1, 1], "Yellow": [null, "drowned", null, 1, 1], "Axe": [[2, 2], false], "Dagger": [[2, 5], false], "MagicStaff": [[5, 2], false], "Helmet": [[5, 5], false]}'
>>> 
```