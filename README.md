# Connect Four Game

## Description
This program creates a "Connect Four" game (a la the classic 1974 Milton Bradley
game). If you are unfamiliar with the game, rules may be found at
https://en.wikipedia.org/wiki/Connect_Four.

By default, one player will be human and the other player will be a computer
player, whose AI is contained in the file "connect4player.py". This will have a
class called ComputerPlayer. Computer Player will use the minimax algorithm in 
order to find the best location for the computer to play within the bounds of
the number of plies allowed. To optimize the minimax game, alpha-beta pruning
is used to decrease the search space.

This is version 2.0, which includes a text-based mode. This isn't as fun, but 
will work if you can't get the graphics dependencies working.

## Play Game
Make sure to have these installs:
```
pip install tkinter
pip install numpy
```

Then run this on the terminal to play the game:
```
python3 connect4.py
```

## Further Work
There can be further work to improve this project by using different ways to play
the Connect Four game such as using a deep learning model that is not limited by
the number of plies it is allowed to look ahead.
